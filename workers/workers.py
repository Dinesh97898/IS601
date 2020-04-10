from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import and_

from app import admin_only, db
from core.forms import PurchaseForm
from core.models import Purchase, PurchaseType
from workers.models import Worker, Promotion

workers_bp = Blueprint('workers', __name__, template_folder='templates')


@workers_bp.route('/gather/<int:resource_id>')
def pick_to_gather(resource_id):
    workers = Worker.query.filter_by(user_id=current_user.id).order_by(Worker.health.desc(), Worker.next_action.asc()).all()
    return render_template("workers.html", resource_id=resource_id, workers=workers)


@workers_bp.route('/lfw/<int:page>')
@workers_bp.route('/lfw')
def looking_for_work(page=1):
    from auth.models import User
    user_id = User.get_sys_user_id
    workers = Worker.query.filter_by(user_id=user_id).paginate(page, 12, False)
    next_url = url_for('workers.looking_for_work', page=workers.next_num) \
        if workers.has_next else None
    prev_url = url_for('workers.looking_for_work', page=workers.prev_num) \
        if workers.has_prev else None
    return render_template("workers.html", workers=workers.items, prev_url=prev_url, next_url=next_url, current_page=page)


@workers_bp.route('/fired')
@login_required
@admin_only
def get_fired_workers():
    from auth.models import User
    user_id = User.get_sys_user_id
    print('worker sys id ')
    print(user_id)
    workers = Worker.query.filter(and_(Worker.user_id==user_id, Worker.previous_user_id==user_id)).all()
    return render_template("workers.html", workers=workers)


@workers_bp.route('/fire/<int:worker_id>')
@login_required
def fire(worker_id):
    worker = Worker.query.get(int(worker_id))
    if worker is not None:
        if worker.user_id == current_user.id:
            worker.fire()
            flash("You fired " + worker.name)
        else:
            flash("You can't fire a worker that isn't part of your crew.")
    else:
        flash("Couldn't find particular worker")
    return redirect(url_for('workers.my_workers'))


@workers_bp.route('/hire', methods=['GET', 'POST'])
@login_required
def hire_random():
    # TODO add a cost
    cost = current_user.get_hire_cost()
    print('cost ' + str(cost))
    form = PurchaseForm()
    balance = current_user.get_coins()
    if form.validate_on_submit():
        if cost <= balance:
            _purchase = Purchase()
            _purchase.user_id = current_user.id
            _purchase.cost = cost
            _purchase.purchase_type = PurchaseType.WORKER

            worker = Worker()
            worker.generate(current_user.id)
            flash('Congrats you hired ' + worker.name)
            current_user.make_purchase(cost)
            db.session.commit()
            # balance = current_user.get_coins()
            return redirect(url_for('workers.my_workers'))
        else:
            flash("Sorry you can't afford to hire any more workers")
    else:
        pass
    form.cost.data = cost

    return render_template('hire_worker.html', form=form, balance=balance), 200


@workers_bp.route('/promote/<int:worker_id>')
@login_required
def promote_worker(worker_id):
    worker = Worker.query.get(int(worker_id))
    if worker is not None:
        print('attempting promote')
        promo_status = worker.promote()
        if promo_status is False:
            flash("Sorry, you can't afford to promote " . worker.name)
        elif promo_status == Promotion.NONE:
            flash(worker.name + " is already at maximum skills.")
        elif promo_status == Promotion.INCREASED_SKILL:
            flash("Congrats " + worker.name + " increased their skill")
        elif promo_status == Promotion.INCREASED_EFFICIENCY:
            flash("Congrats " + worker.name + " increased their efficiency")
        elif promo_status == Promotion.MAXED_SKILL:
            flash("Congrats " + worker.name + " maxed their skill")
        elif promo_status == Promotion.MAXED_EFFICIENCY:
            flash("Congrats " + worker.name + " maxed their efficiency")
    return redirect(url_for('workers.my_workers'))


@workers_bp.route('/crew')
@login_required
def my_workers():
    print('current user: ' + str(current_user.id))
    workers = Worker.query.filter_by(user_id=current_user.id).all()
    print('results: ' + str(len(workers)))
    return render_template("workers.html", workers=workers)
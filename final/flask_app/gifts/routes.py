from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from ..models import GiftRequest, MatchedGift
from ..forms import UpdateTrackingForm, CommentForm

gifts = Blueprint("gifts", __name__)

@gifts.route("/")
def index():
    return render_template("index.html")

@gifts.route("/request", methods=["GET", "POST"])
@login_required
def request_gift():
    if request.method == "POST":
        data = request.form.to_dict(flat=False)
        data["requester"] = current_user
        data["matched"] = False
        for k, v in data.items():
            if isinstance(v, list) and len(v) == 1:
                data[k] = v[0]

        giftRequest = GiftRequest(**data)
        giftRequest.save()

        pending_gifts = GiftRequest.objects(matched=False)
        for g in pending_gifts:
            if g.requester != current_user:
                userA = current_user
                userB = g.requester

                g.matched = True
                giftRequest.matched = True
                g.save()
                giftRequest.save()

                giftA = MatchedGift(giftReceiver=userA, giftSender=userB, gift=giftRequest, status="Waiting for Gift Selection")
                giftA.save()
                giftB = MatchedGift(giftReceiver=userB, giftSender=userA, gift=g, status="Waiting for Gift Selection")
                giftB.save()

                return redirect(url_for("gifts.matched_gift", id=giftB.id))
    return render_template("request.html")

@gifts.route("/matched/<id>", methods=["GET", "POST"])
@login_required
def matched_gift(id):
    try:
        gift = MatchedGift.objects(id=id).first()
    except Exception:
        return redirect(url_for("gifts.index"))

    if gift is None or gift.giftSender != current_user:
        return redirect(url_for("gifts.index"))


    if request.method == "POST":
        gift.giftName = request.form.get("chosenGift")
        gift.status = "Waiting for Shipping Information"
        gift.save()
        return redirect(url_for("users.account"))
    
    choice = gift.gift.gifts
    return render_template("matched.html", choice=choice)

@gifts.route("/gift/detail/<id>", methods=["GET", "POST"])
@login_required
def detail(id):
    try:
        gift = GiftRequest.objects(id=id).first()
        match = MatchedGift.objects(gift=gift).first()
    except Exception:
        return redirect(url_for("gifts.index"))

    form = UpdateTrackingForm()
    commentform = CommentForm()

    if gift is None:
        return redirect(url_for("gifts.index"))

    if gift.matched and match.giftName is None and match.giftSender == current_user:
        return redirect(url_for("gifts.matched_gift", id=match.id))

    if form.validate_on_submit():
        match.tracking = form.tracking.data
        match.status = "Tracking Info Entered"
        match.save()
        flash("Tracking information updated")
        return redirect(url_for("gifts.detail", id=id))

    if commentform.validate_on_submit():
        match.comment = commentform.pagedown.data
        match.status = "Comment Received"
        match.save()
        return redirect(url_for("gifts.detail", id=id))
    
    if request.method == "POST":
        match.status = "Gift Received"
        match.save()
        return redirect(url_for("gifts.detail", id=id))

    if gift.requester != current_user and (match is not None and match.giftSender != current_user):
        return redirect(url_for("gifts.index"))
    
    if gift.matched and match.giftSender == current_user and "Received" not in match.status:
        return render_template("giftdetail.html", g=gift, m=match, form=form)
    elif gift.matched:
        if match.giftReceiver == current_user and match.status == "Gift Received":
            return render_template("giftdetail.html", g=gift, m=match, c=commentform)
        else:
            return render_template("giftdetail.html", g=gift, m=match)
    else:
        return render_template("giftdetail.html", g=gift)

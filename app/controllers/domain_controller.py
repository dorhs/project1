from flask import Blueprint, session, render_template, request, abort
from app.services import domain_service as dms
from app.forms import AddDomainForm, BulkUploadForm
from app.vers import *


@domain_bp.route('/add_domain', methods=["GET", "POST"])
def add_domain():
    if not userError():
        logger.debug("Receive an 403 - Forbidden")
        return abort(403)
    form = AddDomainForm()
    msg = ""
    if form.validate_on_submit():
        domain_name = form.domain_name.data
        username = session.get("username", None)
        status, msg = dms.add_domain(domain=domain_name, username=username)
        if status:
            return render_template('add_domain.html', form=form, error=msg, Mode=True)
        else:
            return render_template('add_domain.html', form=form, error=msg, Mode=False)
    return render_template('add_domain.html', form=form, error=msg, Mode=False)


@domain_bp.route('/bulk_upload', methods=["GET", "POST"])
def bulk_upload_domains():
    if not userError():
        logger.debug("Receive an 403 - Forbidden")
        return abort(403)

    form = BulkUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        username = session.get("username", None)
        status, msg = dms.bulk_upload_domains(
            file=file.read().decode().split("\r\n"),
            username=username
        )
        if status:
            return render_template('bulk_upload.html', form=form, error=msg, Mode=True)
        else:
            return render_template('bulk_upload.html', form=form, error=msg, Mode=False)
    return render_template('bulk_upload.html', form=form, error="", Mode=False)


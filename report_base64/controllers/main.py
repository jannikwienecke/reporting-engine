from odoo.addons.web.controllers import main as report
from odoo.http import content_disposition, route, request
from odoo.tools.safe_eval import safe_eval
import base64

import json
import time


class ReportController(report.ReportController):
    @route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        report = request.env['ir.actions.report']._get_report_from_name(reportname)
        context = dict(request.env.context)

        if converter == 'base64':
            print( report, context, data)
            print(report.with_context)
            print(docids)
            try:
                # failed here
                pdf = report.with_context(context).render_qweb_pdf(docids, data=data)[0]
            except Exception as e:
                print(e)

            base64String = base64.b64encode(pdf)
            pdfhttpheaders = [('Content-Type', 'text/html'), ('Content-Length', len(base64String))]
            return request.make_response(base64String, headers=pdfhttpheaders)
        else:
            return super(ReportController, self).report_routes(
            reportname, docids, converter, **data)

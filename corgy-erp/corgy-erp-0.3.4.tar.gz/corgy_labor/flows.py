from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from viewflow import frontend

from .models import PayrollProcess, LaborStatementProcess

@frontend.register
class LaborStatementProcessFlow(Flow):

    process_class = LaborStatementProcess

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.end)
    )

    end = flow.End()

@frontend.register
class PayrollProcessFlow(Flow):

    process_class = PayrollProcess

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (flow.Handler(this.monthly_closing).Next(this.end))

    end = flow.End()

    def monthly_closing(self, activation):
        print(activation.process.text)
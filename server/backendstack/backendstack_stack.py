import os
import subprocess
from aws_cdk import (
    Stack,
    # CfnOutput,
    aws_lambda as _lambda,
    Duration,
    aws_events as events,
    aws_apigateway as api_gateway,
    aws_logs as logs,
    aws_events_targets as targets,
)
from constructs import Construct


from form_submission.env import get_environment as form_submission_environment
from email_cron.env import get_environment as email_cron

ENV = os.getenv("ENVIRONMENT")


class BackendstackStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "BackendstackQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # form_submission_function = aws_lambda.Function(
        #     self,
        #     id="form_submission_function",
        #     code=aws_lambda.Code.from_asset("./form_submission"),
        #     handler="app.handler",
        #     runtime=aws_lambda.Runtime.PYTHON_3_10,
        # )

        fn_form_submission_function = _lambda.Function(
            self,
            id="form_submission",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="app.handler",
            code=_lambda.Code.from_asset("./form_submission"),
            environment=form_submission_environment(),
            layers=[self.create_dependencies_layer(self.stack_name, "form_submission")],
            timeout=Duration.seconds(300),
            memory_size=128,
            # vpc=vpc,
            log_retention=logs.RetentionDays.ONE_DAY,
        )

        fn_email_cron = _lambda.Function(
            self,
            id="email_cron",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="app.handler",
            code=_lambda.Code.from_asset("./email_cron"),
            environment=email_cron(),
            layers=[self.create_dependencies_layer(self.stack_name, "email_cron")],
            timeout=Duration.seconds(300),
            memory_size=128,
            # vpc=vpc,
            log_retention=logs.RetentionDays.ONE_DAY,
        )

        base_api = api_gateway.RestApi(
            self, "backendstack_api_gateway", rest_api_name="backendstack_api_gateway"
        )

        form_submission_api = base_api.root.add_resource(
            "form_submission",
            default_cors_preflight_options=api_gateway.CorsOptions(
                allow_methods=["POST", "OPTIONS"],
                allow_origins=api_gateway.Cors.ALL_ORIGINS,
            ),
        )
        form_submission_lambda_integration = api_gateway.LambdaIntegration(
            fn_form_submission_function,
            proxy=False,
            integration_responses=[
                api_gateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": "'*'"
                    },
                )
            ],
        )
        form_submission_api.add_method(
            "POST",
            form_submission_lambda_integration,
            method_responses=[
                api_gateway.MethodResponse(
                    status_code="200",
                    response_parameters={
                        "method.response.header.Access-Control-Allow-Origin": True
                    },
                )
            ],
        )

        if ENV == "prod":
            # having daily lambda cron only for prod
            rule = events.Rule(
                self,
                "email_cron_scheduler",
                schedule=events.Schedule.cron(
                    minute="00", hour="00", month="*", week_day="*", year="*"
                ),
                # schedule=events.Schedule.rate(aws_cdk_duration.hours(24)),
            )
            rule.add_target(
                targets.LambdaFunction(
                    fn_email_cron,
                    event=events.RuleTargetInput.from_object(
                        {"event_type": "scheduler"}
                    ),
                )
            )

    def create_dependencies_layer(
        self, project_name, function_name: str
    ) -> _lambda.LayerVersion:
        requirements_file = f"{function_name}/requirements.txt"
        output_dir = f"../.build/{function_name}"

        if not os.environ.get("SKIP_PIP"):
            subprocess.check_call(
                f"pip install -r {requirements_file} -t {output_dir}/python".split()
            )

        layer_id = f"{project_name}-{function_name}-dependencies"
        layer_code = _lambda.Code.from_asset(output_dir)

        return _lambda.LayerVersion(self, layer_id, code=layer_code)

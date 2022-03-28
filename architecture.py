import diagrams
import diagrams.aws.compute
import diagrams.aws.database
import diagrams.aws.integration
import diagrams.aws.security


with diagrams.Diagram('AWS Auditor', show=False, direction='TB'):
    auditor = diagrams.aws.compute.Lambda('AuditorLambdaFunction')
    (
        diagrams.aws.integration.Eventbridge('AuditSchedule') >>
        auditor >>
        diagrams.aws.database.DynamodbTable('AuditInventory')
    )
    with diagrams.Cluster('IAM'):
        auditor_role = diagrams.aws.security.IAMRole('AuditorLambdaRole')
        (
            diagrams.aws.security.IAMPermissions('ResourcePermissions') -
            auditor_role >> diagrams.Edge() << auditor
        )
import diagrams
import diagrams.aws.compute
import diagrams.aws.database
import diagrams.aws.integration
import diagrams.aws.security


with diagrams.Diagram('Aws Auditor', show=False, director='TB'):
    auditor = diagrams.aws.compute.Lambda('AuditorLambdaFunction')
    auditor_role = diagrams.aws.security.IAMRole('AuditorLambdaRole')
    (
        diagrams.aws.integration.Eventbridge('AuditSchedule') >>
        auditor >>
        diagrams.aws.database.DynamodbTable('AuditInventory')
    )
    (
        auditor <<
        auditor_role -
        diagrams.aws.security.IAMPermissions('ResourcePermissions')
    )
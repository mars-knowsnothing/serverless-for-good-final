SAMPLE_EVENT = {
  "SchemaVersion": "2018-10-08",
  "Id": "arn:aws:securityhub:ap-southeast-1:592336536196:subscription/aws-foundational-security-best-practices/v/1.0.0/S3.2/finding/5b773e58-af0b-467e-a3ca-ee49048200c7",
  "ProductArn": "arn:aws:securityhub:ap-southeast-1::product/aws/securityhub",
  "ProductName": "Security Hub",
  "CompanyName": "AWS",
  "Region": "ap-southeast-1",
  "GeneratorId": "aws-foundational-security-best-practices/v/1.0.0/S3.2",
  "AwsAccountId": "592336536196",
  "Types": [
    "Effects/Data Exposure/AWS-Foundational-Security-Best-Practices"
  ],
  "FirstObservedAt": "2022-09-21T01:43:47.628Z",
  "LastObservedAt": "2022-09-21T01:43:51.883Z",
  "CreatedAt": "2022-09-21T01:43:47.628Z",
  "UpdatedAt": "2022-09-21T01:43:47.628Z",
  "Severity": {
    "Product": 90,
    "Label": "CRITICAL",
    "Normalized": 90,
    "Original": "CRITICAL"
  },
  "Title": "S3.2 S3 buckets should prohibit public read access",
  "Description": "This AWS control checks whether your S3 buckets allow public read access by evaluating the Block Public Access settings, the bucket policy, and the bucket access control list (ACL).",
  "Remediation": {
    "Recommendation": {
      "Text": "For directions on how to fix this issue, consult the AWS Security Hub Foundational Security Best Practices documentation.",
      "Url": "https://docs.aws.amazon.com/console/securityhub/S3.2/remediation"
    }
  },
  "ProductFields": {
    "StandardsArn": "arn:aws:securityhub:::standards/aws-foundational-security-best-practices/v/1.0.0",
    "StandardsSubscriptionArn": "arn:aws:securityhub:ap-southeast-1:592336536196:subscription/aws-foundational-security-best-practices/v/1.0.0",
    "ControlId": "S3.2",
    "RecommendationUrl": "https://docs.aws.amazon.com/console/securityhub/S3.2/remediation",
    "RelatedAWSResources:0/name": "securityhub-s3-bucket-public-read-prohibited-a83b9f95",
    "RelatedAWSResources:0/type": "AWS::Config::ConfigRule",
    "StandardsControlArn": "arn:aws:securityhub:ap-southeast-1:592336536196:control/aws-foundational-security-best-practices/v/1.0.0/S3.2",
    "aws/securityhub/ProductName": "Security Hub",
    "aws/securityhub/CompanyName": "AWS",
    "aws/securityhub/annotation": "The S3 bucket policy allows public read access.",
    "Resources:0/Id": "arn:aws:s3:::s3-finding-test",
    "aws/securityhub/FindingId": "arn:aws:securityhub:ap-southeast-1::product/aws/securityhub/arn:aws:securityhub:ap-southeast-1:592336536196:subscription/aws-foundational-security-best-practices/v/1.0.0/S3.2/finding/5b773e58-af0b-467e-a3ca-ee49048200c7"
  },
  "Resources": [
    {
      "Type": "AwsS3Bucket",
      "Id": "arn:aws:s3:::s3-finding-test",
      "Partition": "aws",
      "Region": "ap-southeast-1",
      "Details": {
        "AwsS3Bucket": {
          "OwnerId": "a0e08597d99671b6c2462a34f2b593c277343bc9d5ddecc395d3eac4e0efb73c",
          "CreatedAt": "2022-09-21T01:40:56.000Z"
        }
      }
    }
  ],
  "Compliance": {
    "Status": "FAILED"
  },
  "WorkflowState": "NEW",
  "Workflow": {
    "Status": "NEW"
  },
  "RecordState": "ACTIVE",
  "FindingProviderFields": {
    "Severity": {
      "Label": "CRITICAL",
      "Original": "CRITICAL"
    },
    "Types": [
      "Effects/Data Exposure/AWS-Foundational-Security-Best-Practices"
    ]
  }
}
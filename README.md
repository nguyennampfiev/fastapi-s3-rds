# FastAPI S3 RDS Project

A FastAPI application that integrates with AWS S3 for file storage and PostgreSQL RDS for database management, featuring automated CI/CD pipeline.

## 🚀 Features

* File upload/download with AWS S3 integration
* PostgreSQL database with SQLAlchemy ORM
* Automated CI/CD pipeline using GitHub Actions
* Deployment to AWS EC2 / ECS Fargate
* Modern dependency management with `uv`

## 🏗️ Project Structure

```
fastapi-s3-rds/
├── app/
│   ├── api/
│   │   └── endpoints/
│   ├── core/
│   ├── db/
│   │   ├── models.py
│   │   └── base.py
│   └── schemas/
├── tests/
├── .github/
│   └── workflows/
│       └── deploy.yml
└── requirements.txt
```

## 🛠️ Technology Stack

* **FastAPI**: Modern Python web framework
* **SQLAlchemy**: SQL toolkit and ORM
* **AWS S3**: File storage
* **AWS RDS**: PostgreSQL database
* **GitHub Actions**: CI/CD pipeline
* **uv**: Fast Python package installer and resolver

## 🔄 CI/CD Pipeline

Our deployment process uses GitHub Actions with two main jobs:

### 1. Test Job

* Checks out the code
* Sets up Python environment using `uv`
* Installs dependencies
* Runs pytest with the following configurations:

  * PostgreSQL database connection
  * AWS S3 credentials
  * Region: eu-north-1

### 2. Deploy Job

* Triggers after successful test completion
* Deploys to AWS EC2 instance
* Performs the following steps:

  * Updates code from main branch
  * Syncs dependencies using `uv`
  * Restarts FastAPI service

## 🏃‍♂️ Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi-s3-rds.git
cd fastapi-s3-rds
```

2. Set up environment variables:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your_bucket_name
AWS_REGION=eu-north-1
```

3. Install dependencies:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
```

4. Run the application locally:

```bash
uvicorn main:app --reload
```

**Note:** When using Gunicorn for production, use:

```dockerfile
CMD ["gunicorn", "app.main:app", "--workers", "2", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
```

## 🔐 AWS Setup Required

1. **EC2 Instance**

   * Ubuntu server
   * Configured with SSH access
   * Security group with appropriate ports open

2. **S3 Bucket**

   * Created in eu-north-1 region
   * Proper IAM permissions configured

3. **RDS PostgreSQL**

   * Database instance running
   * Proper security group settings
   * Network access configured

## 📝 Environment Variables Required

* `DATABASE_URL`: PostgreSQL connection string
* `AWS_ACCESS_KEY_ID`: AWS access key
* `AWS_SECRET_ACCESS_KEY`: AWS secret key
* `S3_BUCKET_NAME`: AWS S3 bucket name
* `AWS_REGION`: AWS region (default: eu-north-1)

## 🔒 Security Notes

* SSH keys are managed through GitHub Secrets
* AWS credentials are stored securely in GitHub Secrets
* Database credentials are managed through environment variables

---

## ⚠️ Notes for Developers

* **Pydantic v2:** The old `orm_mode` is renamed to `from_attributes`. Update your models accordingly to avoid warnings.
* **Local & EC2 Gunicorn Usage:** Use the CMD above to ensure proper FastAPI worker handling. Without `UvicornWorker`, you may see errors like: `FastAPI.__call__() missing 1 required positional argument: 'send'`.

---

## 🚀 Deployment on AWS ECS (Fargate)

You can deploy the FastAPI app using Docker, AWS ECR, ECS, and Secrets Manager.

### 1. Build Docker Image

```bash
docker build -t fastapi-s3-rds .
```

### 2. Tag Image for ECR

```bash
docker tag fastapi-s3-rds:latest 390844761221.dkr.ecr.eu-north-1.amazonaws.com/fastapi-s3-rds:latest
```

### 3. Push to ECR

```bash
docker push 390844761221.dkr.ecr.eu-north-1.amazonaws.com/fastapi-s3-rds:latest
```

### 4. Configure AWS Secrets Manager

Store sensitive variables as secrets:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `DATABASE_URL`
* `S3_BUCKET_NAME`
* `AWS_REGION`

### 5. Grant ECS Task Execution Role Access

Attach a policy to your ECS task execution role to read secrets:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
      "Resource": ["arn:aws:secretsmanager:eu-north-1:390844761221:secret:fastapi_*"]
    }
  ]
}
```

### 6. ECS Task Definition

Use `task-def.json` with:

* Image: `390844761221.dkr.ecr.eu-north-1.amazonaws.com/fastapi-s3-rds:latest`
* Network mode: `awsvpc`
* CPU & memory allocations
* Container port 8000
* Secrets from Secrets Manager

### 7. Create ECS Service

```bash
aws ecs create-service \
  --cluster fastapi-cluster \
  --service-name fastapi-service \
  --task-definition fastapi-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxx],securityGroups=[sg-xxxx],assignPublicIp=ENABLED}"
```

### 8. Open Security Group for Port 8000

```bash
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxx \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0
```

### 9. Access the Application

Open in your browser:

```
http://<public-ip>:8000/docs
```

Swagger UI should load and show all your API endpoints.

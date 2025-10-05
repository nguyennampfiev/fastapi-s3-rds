# FastAPI S3 RDS Project

A FastAPI application that integrates with AWS S3 for file storage and PostgreSQL RDS for database management, featuring automated CI/CD pipeline.

## 🚀 Features

- File upload/download with AWS S3 integration
- PostgreSQL database with SQLAlchemy ORM
- Automated CI/CD pipeline using GitHub Actions
- Deployment to AWS EC2
- Modern dependency management with `uv`

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

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **AWS S3**: File storage
- **AWS RDS**: PostgreSQL database
- **GitHub Actions**: CI/CD pipeline
- **uv**: Fast Python package installer and resolver

## 🔄 CI/CD Pipeline

Our deployment process uses GitHub Actions with two main jobs:

### 1. Test Job
- Checks out the code
- Sets up Python environment using `uv`
- Installs dependencies
- Runs pytest with the following configurations:
  - PostgreSQL database connection
  - AWS S3 credentials
  - Region: eu-north-1

### 2. Deploy Job
- Triggers after successful test completion
- Deploys to AWS EC2 instance
- Performs the following steps:
  - Updates code from main branch
  - Syncs dependencies using `uv`
  - Restarts FastAPI service

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

4. Run the application:
```bash
uvicorn main:app --reload
```

## 🔐 AWS Setup Required

1. **EC2 Instance**
   - Ubuntu server
   - Configured with SSH access
   - Security group with appropriate ports open

2. **S3 Bucket**
   - Created in eu-north-1 region
   - Proper IAM permissions configured

3. **RDS PostgreSQL**
   - Database instance running
   - Proper security group settings
   - Network access configured

## 🚀 Deployment

Deployment is automated via GitHub Actions when pushing to the main branch:
1. Tests are run
2. On success, code is deployed to EC2
3. FastAPI service is automatically restarted

## 📝 Environment Variables Required

- `DATABASE_URL`: PostgreSQL connection string
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `S3_BUCKET_NAME`: AWS S3 bucket name
- `AWS_REGION`: AWS region (default: eu-north-1)

## 🔒 Security Notes

- SSH keys are managed through GitHub Secrets
- AWS credentials are stored securely in GitHub Secrets
- Database credentials are managed through environment variables
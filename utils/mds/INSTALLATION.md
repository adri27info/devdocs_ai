## Requirements

Before starting, you need to have the following accounts and tools:

- **[Gmail](https://gmail.com/):** Required to send emails for new user accounts within the app. Make sure to temporarily disable your antivirus on Windows to prevent SSL certificate errors when sending emails.

- **[Docker Desktop](https://www.docker.com/products/docker-desktop/):** Required to run the application locally.

- **[Stripe](https://stripe.com/):** Required because users in the app can upgrade their subscription plans using this service.

- **[Open Router](https://openrouter.ai/):** Required because the app uses a large language model (LLM) from Open Router to generate documentation.

- **[Amazon Web Services - AWS](https://aws.amazon.com/):** Required for services like:

  - IAM (Identity and Access Management) for permissions

  - S3 (Simple Storage Service) for storage

  - CloudFront for caching, security, and content delivery

  - EC2 (Elastic Compute Cloud) for running instances

  - Systems Manager for executing commands and managing resources

## Gmail

To use Gmail, you need to create an account. Once your account is ready, follow these steps:

1. Go to [Google Account Settings](https://myaccount.google.com).

2. Enable **Two-Factor Authentication (2FA)**.

3. After enabling 2FA, go to the **App Passwords** section and do the following:

   - Give your app a name.

   - Copy the generated app password. Example:

   ```
   EMAIL_HOST_USER="your_gmail@gmail.com"
   EMAIL_HOST_PASSWORD="your_generated_app_password"  # Your generated app password
   EMAIL_HOST="smtp.gmail.com"
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   ```

## Docker Desktop

1. Go to [Docker Desktop](https://www.docker.com/products/docker-desktop/).

2. Download Docker Desktop for your operating system (e.g., Windows, macOS).

3. During installation, keep the following in mind:

   - Use Docker Desktop for personal use.

   - Use the **WSL 2 backend** (for Windows).

   - Ensure integration with your WSL 2 distribution is enabled (e.g., Ubuntu). You can enable this in Docker Desktop under **Resources > WSL Integration**.

## Stripe

To use Stripe, you need to create an account. In this project, I signed in using my Gmail account. Once inside Stripe, follow these steps:

1. Go to [Stripe](https://stripe.com/).

2. Create a **Test Environment** (enable **TEST mode**).

   - In the demo video, the test card `4242 4242 4242 4242` is used. This card is for testing only and does not generate actual charges.

3. Once in Test Mode, copy the following API keys from the right side of the dashboard:

   ```
   STRIPE_SECRET_KEY="sk_test_XXXXXXXXX"
   STRIPE_PUBLISHABLE_KEY="pk_test_XXXXX"
   ```

4. Create a new product linked to your app:

- Example: a $20 subscription called Premium Plan.

- To create the product, go to Product Catalog > Create New Product, then provide:

  - Product name

  - Description

  - Attachment (optional)

  - Pricing: One-time payment (important)

  - Price: e.g., $20

  - Finally, save the product.

5. After creating the product, go to the Pricing section and copy the generated Price ID:

   ```
   STRIPE_PRICE_ID="price_XXXXXX"
   ```

6. Finally, configure the backend environment variables for Stripe. Example:

   ```
   USE_STRIPE=True
   STRIPE_SECRET_KEY="sk_test_XXXX"
   STRIPE_PUBLISHABLE_KEY="pk_test_XXXX"
   STRIPE_PRICE_ID="price_XXXXXX"
   ```

## Open Router

To use Open Router, you need to create an account. In this project, I signed in using my Gmail account. Once inside Open Router, follow these steps:

1. Create an **API key** and give it a name. Example:

   ```
   OPENROUTER_API_KEY="sk-or-v1-XXXXX"
   ```

2. Keep in mind that when I created my Open Router account, there were some free credits available for using paid LLMs. In this app, I opted to use the mistral-7b-instruct:free model, which is free at the moment.

- If you are following this guide in the future and this model is no longer free, update the backend environment variable accordingly.

3. Finally, configure the backend environment variables for Open Router. Example:

   ```
   OPENROUTER_API_KEY="sk-or-v1-XXXX"
   OPENROUTER_BASE_URL="https://openrouter.ai/api/v1/chat/completions"
   OPENROUTER_MODEL="mistralai/mistral-7b-instruct:free"
   IMAGE_GHCR="ghcr.io/adri27info/fastapi-llm:latest"
   ```

## AWS

To use AWS, you need to create an account. Follow these steps:

1. Go to [AWS](https://aws.amazon.com/).

2. Navigate to the **Create an Account** section.

3. Fill in all the required information, such as account name, country, email, etc.

   - At some point, to use AWS Free Tier services, you will be asked to provide a credit card for a $1 verification charge.

   - This is required to access services like IAM, S3, CloudFront, EC2, and Systems Manager within the app.

   - Note: The Free Tier allows you to use these services at no cost as long as you stay within usage limits. If you exceed them, charges may apply.

4. Once all the required information is completed, your AWS account will be ready to use.

## AWS - IAM

AWS Identity and Access Management (IAM) is a service that allows you to manage users, permissions, and policies within your AWS account. Once we understand its purpose, we will create a user with specific permissions and a role with an assigned policy.

1. Go to the **IAM** section in the AWS console.

2. Create a new user:

   - Provide a username.

   - Attach the following permission policies to the user:

     - `AmazonEC2FullAccess`

     - `AmazonS3FullAccess`

     - `AmazonSSMFullAccess`

     - `CloudFrontFullAccess`

   - Click **Next** and create the user.

3. Once the user is created, generate access keys:

   - Go to **Security Credentials > Create Access Key**.

   - Select **Use Case: Local Code**.

   - You will obtain two keys (example):

   ```
   AWS_ACCESS_KEY_ID="XXXXXXXX"
   AWS_SECRET_ACCESS_KEY="XXXXXXXX"
   ```

4. Next, create a Role:

- Go to the Roles section and click Create Role.

- Choose AWS Service as the trusted entity and select EC2.

- Select the use case EC2 Role for AWS Systems Manager.

- Attach the following policy to the role: AmazonSSMManagedInstanceCore.

- Provide a name and description for the role.

- Click Create Role to finalize.

## AWS - S3

Amazon S3 (Simple Storage Service) is a cloud object storage service offered by Amazon Web Services (AWS). It allows you to store and retrieve any amount of data at any time from anywhere on the Internet. Once we understand its purpose, we can create a bucket.

1. Go to the **S3** section in the AWS console.

2. Click **Create Bucket**.

   - Provide a name for the bucket.

   - Select a region.

   - Disable the **ACL** option.

   - Enable **Block all public access**.

   - Leave the other settings as default and click **Create Bucket**.

3. After creating the bucket, create the following folders inside it:

   - media

   - attachments - (media/attachments)

   - user - (media/attachments/user)

   - profile - (media/attachments/user/profile)

- Once all folders are created the route looks like this:

  - first_folder_of_your_bucket/media/attachments/user/profile

- Enter the **profile** folder and upload the file `personal_remote.png`.

  - This image is located in the backend `static` folder and represents a simple user avatar.

  - This is the only manual configuration required at bucket creation because the app will create additional folders automatically through backend environment variables.

4. Configure the bucket policy:

- Go to the **Permissions** tab, then **Bucket Policy**, and click **Edit** to add the following policy:

  ```json
  {
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
      {
        "Sid": "AllowCloudFrontServicePrincipal",
        "Effect": "Allow",
        "Principal": {
          "Service": "cloudfront.amazonaws.com"
        },
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::<YOUR-BUCKET-NAME>/*",
        "Condition": {
          "StringEquals": {
            "AWS:SourceArn": "arn:aws:cloudfront::<YOUR-AWS-ACCOUNT-ID>:distribution/<YOUR-DISTRIBUTION-ID>"
          }
        }
      }
    ]
  }
  ```

5. Replace the placeholders inside < > with your actual values:

- YOUR-BUCKET-NAME: Name of your newly created bucket

- YOUR-AWS-ACCOUNT-ID: Your AWS account ID

- YOUR-DISTRIBUTION-ID: The CloudFront distribution ID you will create next

## AWS - CloudFront

Amazon CloudFront is AWS's content delivery network (CDN) service. It delivers files and web content quickly, securely, and efficiently to users worldwide. Once we understand its purpose, we can create a distribution.

1. Go to the **CloudFront** section in the AWS console.

2. Click **Create Distribution**.

   - Provide a name for the distribution.

   - Set the **Distribution Type** to **Single Website or App**.

   - Select **Amazon S3** as the **Origin Type**.

   - In the **Origin** section, choose the bucket you created earlier.

3. In the **Settings** section:

   - Enable **Allow Private S3 Bucket Access to CloudFront**.

   - Leave WAF disabled.

4. Click **Create Distribution**.

5. Once the distribution is created, copy its ID and use it in the bucket policy you configured in the previous section.

### Backend Environment Variables for AWS, S3, and CloudFront

```
# AWS
AWS_ACCESS_KEY_ID="your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
AWS_STORAGE_BUCKET_NAME="your_s3_bucket_name"
AWS_LOCATION="your_first_folder_of_your_s3_bucket"
AWS_MEDIA_LOCATION="your_first_folder_of_your_s3_bucket/media"
AWS_USER_IMAGE_BUCKET_URL="attachments/user/profile/personal_remote.png"
AWS_DEFAULT_REGION="your_aws_region"
AWS_S3_CUSTOM_DOMAIN="your_cloudfront_domain"
AWS_S3_FILE_OVERWRITE=False
AWS_S3_CACHE_CONTROL="max-age=2592000, public"

# S3
USE_S3=True

# CloudFront
USE_CLOUDFRONT=True
CLOUDFRONT_DISTRIBUTION_ID="your_cloudfront_distribution_id"
```

## AWS - EC2

Amazon EC2 (Elastic Compute Cloud) is AWS's cloud computing service that allows you to launch and manage virtual servers, known as instances. It is the foundation for running applications, websites, APIs, and services in AWS without maintaining your own physical hardware. Once we understand its purpose, we can create an EC2 instance.

1. Go to the **EC2** section in the AWS console.

2. Click **Launch/Create Instance**.

   - Create only **one instance** (IMPORTANT).

   - Provide a name for the instance.

   - Select the operating system (in this example, **Ubuntu Server 22.04**).

   - Choose the instance type, for example, **t3.micro**.

   - Do not select any key pair because we will not connect via SSH. Choose **Proceed without a key pair**.

   - For the firewall, select an existing security group (e.g., **default**).

   - Leave all other settings as default and create the instance.

3. Once the instance is created, go to the **Security Groups** section:

   - Create a new security group.

   - Provide a name and description.

   - Select the correct VPC.

   - Add an inbound rule:

     - Type: Custom TCP

     - Protocol: TCP

     - Port Range: 9000

     - Source: Your current IP

4. Apply the new security group to the instance:

   - Select the instance, go to **Actions > Security > Change Security Groups**, and replace **default** with the new security group.

   - In the same menu, choose **Modify IAM Role** and select the role created earlier in this guide.

5. Stop the instance:

   - Select the instance, go to **Instance State**, and choose **Stop Instance**. Wait until it stops completely.

6. Copy the **Instance ID** for later use. Example:

   - `EC2_INSTANCE_ID="XXXX"`

### Backend Environment Variables for EC2

```
# EC2
USE_EC2=True
EC2_INSTANCE_ID="XXXX"
```

## AWS - SYSTEMS MANAGER

AWS Systems Manager is an AWS service that allows you to centrally and securely manage and automate both cloud and on-premises infrastructure. With it, you can control, configure, monitor, and automate EC2 instances, on-premises servers, and AWS resources without manually connecting to each machine.

> Note: In this project, this section is handled via Django commands, so no additional configuration is needed here.

## BACKEND

Once all services are configured, our `env.sample` for the backend looks like this:

```
# DATABASE
DB_NAME="devdocs_ai"
DB_USER="devdocs_ai_user"
DB_PASSWORD="devdocs_ai_password"
DB_HOST="db"
DB_PORT=5432
DB_MAX_AGE=600

# APP SECRET KEY
SECRET_KEY="your_secret_key_here"

# FRONTEND URL
FRONTEND_URL="http://localhost:8080"

# DEBUG MODE
DEBUG=True

# EMAIL SETTINGS
EMAIL_HOST_USER="your_email@gmail.com"
EMAIL_HOST_PASSWORD="your_email_generated_password"
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT=587
EMAIL_USE_TLS=True

# CELERY
CELERY_BROKER_URL="redis://redis:6379/0"
CELERY_RESULT_BACKEND="redis://redis:6379/0"

# ENTRYPOINTS
ENTRYPOINT_BACKEND="/app/entrypoints/entrypoint_backend.sh"
ENTRYPOINT_CELERY="/app/entrypoints/entrypoint_celery.sh"
ENTRYPOINT_STRIPE_CLI="/app/entrypoints/entrypoint_stripe_cli.sh"

# AWS
AWS_ACCESS_KEY_ID="your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
AWS_STORAGE_BUCKET_NAME="your_s3_bucket_name"
AWS_LOCATION="your_first_folder_of_your_s3_bucket"
AWS_MEDIA_LOCATION="your_first_folder_of_your_s3_bucket/media"
AWS_USER_IMAGE_BUCKET_URL="attachments/user/profile/personal_remote.png"
AWS_DEFAULT_REGION="your_aws_region"
AWS_S3_CUSTOM_DOMAIN="your_cloudfront_domain"
AWS_S3_FILE_OVERWRITE=False
AWS_S3_CACHE_CONTROL="max-age=2592000, public"

# S3
USE_S3=True

# CLOUDFRONT
USE_CLOUDFRONT=True
CLOUDFRONT_DISTRIBUTION_ID="your_cloudfront_distribution_id"

# EC2
USE_EC2=True
EC2_INSTANCE_ID="your_ec2_instance_id"
OPENROUTER_API_KEY="your_openrouter_api_key"
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL="mistralai/mistral-7b-instruct:free"
IMAGE_GHCR="ghcr.io/adri27info/fastapi-llm:latest"

# STRIPE
USE_STRIPE=True
STRIPE_SECRET_KEY="your_stripe_secret_key"
STRIPE_PUBLISHABLE_KEY="your_stripe_publishable_key"
STRIPE_PRICE_ID="your_stripe_product_price_id"
```

## FRONTEND

For the frontend, there are only a few environment variables. The env.sample looks like this:

```
VITE_BACKEND_URL='http://localhost:8000'
VITE_LOGO_URL='/app/logos/devdocs_ai.png'
VITE_IMAGE_NOT_FOUND_URL='/app/logos/image-not-found.png'
VITE_LLM_URL='/app/logos/llm.png'
VITE_USER_PROFILE_IMAGE='/app/user/profile/personal_local.png'
```

This env vars are relationated with the local images using in the frontend dir.

## Start the project

Once you have configured both `.env` files for the frontend and backend, follow these steps to run the app:

1. Clone this project using:

   ```sh
   git clone https://github.com/adri27info/devdocs-ai.git
   ```

2. Start the Docker Desktop application.

3. Open your vs-code.

4. Inside your development environment, you can start the app in two ways:

   - First way: Navigate to the utils/launch directory at the root of the project and run the start.sh script to launch the app. To stop the app, use the down.sh script.

   - Second way: Navigate first to the backend directory and run:

   ```sh
   docker-compose up -d
   ```

   Then, move to the frontend directory and execute the same command. Keep in mind that the first startup may take around 2 to 3 minutes.

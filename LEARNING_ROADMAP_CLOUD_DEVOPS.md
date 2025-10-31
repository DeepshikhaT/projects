# Cloud & DevOps Learning Roadmap (For Telecom Engineers Transitioning)

## 🎯 Reality Check First

**You DON'T need to master everything!**

For job interviews, you need:
- ✅ **Solid understanding** of 3-4 core tools
- ✅ **Basic hands-on** with 3-4 more tools
- ✅ **Awareness** of the rest
- ✅ **1-2 real projects** to show

**Truth:** Most companies use 5-7 of these tools, not all of them.

---

## 📊 Priority Tiers (Based on Market Demand)

### Tier 1: MUST LEARN (Learn NOW - Next 2 months)
**These are in 80%+ of job descriptions:**

1. **Git** - Version control (you already use this!)
2. **Docker** - Containerization
3. **AWS Basics** - EC2, VPC, S3
4. **Terraform** - Infrastructure as Code
5. **Python** - You already know this!

### Tier 2: SHOULD LEARN (Next 3-4 months)
**These are in 50-70% of job descriptions:**

6. **Kubernetes** - Container orchestration
7. **CI/CD** - Jenkins OR GitLab CI (pick one)
8. **Ansible** - Configuration management
9. **Monitoring** - Prometheus + Grafana

### Tier 3: NICE TO HAVE (Next 6+ months)
**These are in 20-40% of job descriptions:**

10. **Azure** - Multi-cloud (after AWS)
11. **ELK Stack** - Logging
12. **Kafka** - Message streaming

---

## 🎓 Complete Learning Plan (12 Weeks to Job-Ready)

### Week 1-2: Git & Docker (MUST HAVE)

**Git (You already use this, just formalize knowledge)**
- **Goal:** Understand branching, merging, rebasing
- **Time:** 5 hours
- **Resources:**
  - FREE: [Git Handbook](https://guides.github.com/introduction/git-handbook/)
  - FREE: [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)
  - Practice: Use Git for all your projects
- **What to Learn:**
  - `git clone`, `commit`, `push`, `pull`
  - Branching: `git branch`, `git checkout`, `git merge`
  - `git rebase`, `git cherry-pick`
  - `.gitignore`, `git stash`
  - Pull requests, code review process
- **Project:** Contribute to an open-source project on GitHub

**Docker (CRITICAL)**
- **Goal:** Build and run containers
- **Time:** 15-20 hours
- **Resources:**
  - FREE: [Docker Official Tutorial](https://docs.docker.com/get-started/)
  - FREE: [Docker for Beginners (YouTube)](https://www.youtube.com/watch?v=fqMOX6JJhGo)
  - PAID: Udemy "Docker Mastery" by Bret Fisher ($15)
- **What to Learn:**
  - Install Docker Desktop
  - Dockerfile basics
  - `docker build`, `docker run`, `docker ps`
  - Docker Compose
  - Volumes, networks
  - Multi-stage builds
- **Hands-On:**
  ```bash
  # Install Docker Desktop
  # Download from docker.com

  # Create Dockerfile for your Python app
  FROM python:3.9
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install -r requirements.txt
  COPY . .
  CMD ["python", "app.py"]

  # Build image
  docker build -t myapp:1.0 .

  # Run container
  docker run -p 5000:5000 myapp:1.0
  ```
- **Project:** Dockerize your EdgeNet-Demo backend

---

### Week 3-4: AWS Fundamentals (TOP PRIORITY)

**AWS (Most Important Cloud Skill)**
- **Goal:** Deploy apps on AWS, understand core services
- **Time:** 30-40 hours
- **Resources:**
  - FREE: [AWS Free Tier Account](https://aws.amazon.com/free/)
  - FREE: [AWS Skill Builder](https://skillbuilder.aws/)
  - PAID: "Ultimate AWS Certified Solutions Architect Associate" Udemy ($15)
  - PAID: A Cloud Guru / Linux Academy (best, but $35/month)
- **What to Learn:**
  - **EC2:** Launch instances, SSH access, security groups
  - **VPC:** Subnets, routing tables, internet gateway
  - **S3:** Create buckets, upload files, static website
  - **Lambda:** Serverless functions
  - **IAM:** Users, roles, policies
  - **RDS:** Managed databases
  - **ELB:** Load balancers
  - **CloudWatch:** Basic monitoring
- **Hands-On:**
  ```bash
  # Week 3 Tasks:
  Day 1-2: Create AWS account, launch first EC2 instance
  Day 3-4: Set up VPC, subnets, security groups
  Day 5-6: Deploy Python app on EC2
  Day 7: Create S3 bucket, host static website

  # Week 4 Tasks:
  Day 1-2: Lambda function basics
  Day 3-4: RDS database setup
  Day 5-6: ELB + Auto Scaling
  Day 7: CloudWatch monitoring
  ```
- **Project:** Deploy your EdgeNet-Demo on AWS
  - EC2 for backend
  - S3 for frontend (static hosting)
  - RDS for database
  - Add to resume!

**AWS Certification (Optional but Valuable):**
- **Recommended:** AWS Certified Solutions Architect - Associate
- **Study time:** 60-80 hours (2-3 months part-time)
- **Cost:** $150 exam fee
- **Worth it?** YES - Opens many doors

---

### Week 5-6: Terraform (Infrastructure as Code)

**Terraform (HIGH DEMAND)**
- **Goal:** Automate AWS infrastructure creation
- **Time:** 20-25 hours
- **Resources:**
  - FREE: [Terraform Official Tutorial](https://learn.hashicorp.com/terraform)
  - FREE: [Terraform Course (YouTube)](https://www.youtube.com/watch?v=7xngnjfIlK4)
  - PAID: Udemy "Terraform for Beginners" ($15)
- **What to Learn:**
  - HCL syntax (Terraform language)
  - Providers (AWS, Azure, etc.)
  - Resources, data sources
  - Variables, outputs
  - State management
  - Modules
  - Terraform commands: `init`, `plan`, `apply`, `destroy`
- **Hands-On:**
  ```hcl
  # main.tf - Create EC2 instance
  provider "aws" {
    region = "us-east-1"
  }

  resource "aws_instance" "web" {
    ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2
    instance_type = "t2.micro"

    tags = {
      Name = "MyWebServer"
    }
  }

  # Commands
  terraform init
  terraform plan
  terraform apply
  terraform destroy
  ```
- **Project:** Re-create your AWS infrastructure with Terraform
  - EC2 instances
  - VPC, subnets
  - Security groups
  - S3 buckets
  - Everything as code!

---

### Week 7-8: Kubernetes Basics (VERY HOT SKILL)

**Kubernetes (K8s)**
- **Goal:** Understand container orchestration, deploy apps
- **Time:** 25-30 hours
- **Resources:**
  - FREE: [Kubernetes Official Tutorial](https://kubernetes.io/docs/tutorials/)
  - FREE: [Kubernetes Crash Course (YouTube)](https://www.youtube.com/watch?v=X48VuDVv0do)
  - PAID: Udemy "Kubernetes for Absolute Beginners" ($15)
  - PAID: "Certified Kubernetes Administrator (CKA)" course ($200)
- **What to Learn:**
  - Kubernetes architecture (master, nodes)
  - Pods, Deployments, Services
  - kubectl commands
  - YAML manifests
  - ConfigMaps, Secrets
  - Persistent Volumes
  - Namespaces
  - Helm (package manager)
- **Setup Options:**
  ```bash
  # Option 1: Minikube (local cluster)
  # Install: https://minikube.sigs.k8s.io/docs/start/
  minikube start
  kubectl get nodes

  # Option 2: Docker Desktop (has K8s built-in)
  # Enable in settings

  # Option 3: AWS EKS (cloud, costs money)
  # Use after comfortable with basics
  ```
- **Hands-On:**
  ```yaml
  # deployment.yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: myapp
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: myapp
    template:
      metadata:
        labels:
          app: myapp
      spec:
        containers:
        - name: myapp
          image: myapp:1.0
          ports:
          - containerPort: 5000

  # Deploy
  kubectl apply -f deployment.yaml
  kubectl get pods
  kubectl get services
  ```
- **Project:** Deploy EdgeNet-Demo on Kubernetes
  - Deployment for backend
  - Service to expose it
  - ConfigMap for configuration
  - Add to resume!

**Kubernetes Certification (HIGH VALUE):**
- **CKA** - Certified Kubernetes Administrator
- **Study time:** 80-100 hours
- **Cost:** $395 (includes retake)
- **Worth it?** YES - $20k+ salary boost

---

### Week 9: CI/CD (Jenkins OR GitLab CI)

**Pick ONE: Jenkins OR GitLab CI**

**Option A: Jenkins (More Jobs)**
- **Goal:** Automate build, test, deploy
- **Time:** 15-20 hours
- **Resources:**
  - FREE: [Jenkins Official Tutorial](https://www.jenkins.io/doc/tutorials/)
  - FREE: [Jenkins Course (YouTube)](https://www.youtube.com/watch?v=7KCS70sCoK0)
- **What to Learn:**
  - Install Jenkins (Docker or EC2)
  - Jenkinsfile (pipeline as code)
  - Build triggers
  - Integration with Git
  - Deploy to AWS
- **Hands-On:**
  ```groovy
  // Jenkinsfile
  pipeline {
      agent any
      stages {
          stage('Build') {
              steps {
                  sh 'pip install -r requirements.txt'
              }
          }
          stage('Test') {
              steps {
                  sh 'pytest tests/'
              }
          }
          stage('Deploy') {
              steps {
                  sh './deploy.sh'
              }
          }
      }
  }
  ```

**Option B: GitLab CI (Easier, Modern)**
- **Goal:** Automate in GitLab
- **Time:** 10-15 hours
- **Resources:**
  - FREE: [GitLab CI Docs](https://docs.gitlab.com/ee/ci/)
  - FREE: [GitLab CI Course (YouTube)](https://www.youtube.com/watch?v=qP8kir2GUgo)
- **What to Learn:**
  - `.gitlab-ci.yml` file
  - Runners
  - Stages and jobs
  - Artifacts
  - Deploy to AWS
- **Hands-On:**
  ```yaml
  # .gitlab-ci.yml
  stages:
    - build
    - test
    - deploy

  build:
    stage: build
    script:
      - pip install -r requirements.txt

  test:
    stage: test
    script:
      - pytest tests/

  deploy:
    stage: deploy
    script:
      - ./deploy.sh
    only:
      - main
  ```

**My Recommendation:** Start with **GitLab CI** (simpler), add Jenkins later if needed.

---

### Week 10: Ansible (Configuration Management)

**Ansible**
- **Goal:** Automate server configuration
- **Time:** 15-20 hours
- **Resources:**
  - FREE: [Ansible Official Tutorial](https://docs.ansible.com/ansible/latest/getting_started/index.html)
  - FREE: [Ansible Course (YouTube)](https://www.youtube.com/watch?v=3RiVKs8GHYQ)
  - PAID: Udemy "Ansible for Beginners" ($15)
- **What to Learn:**
  - Inventory files
  - Playbooks (YAML)
  - Modules
  - Roles
  - Variables
  - Handlers
  - Ansible Vault (secrets)
- **Hands-On:**
  ```yaml
  # playbook.yml
  ---
  - name: Setup Web Server
    hosts: webservers
    become: yes

    tasks:
      - name: Install Nginx
        apt:
          name: nginx
          state: present

      - name: Start Nginx
        service:
          name: nginx
          state: started

      - name: Deploy website
        copy:
          src: index.html
          dest: /var/www/html/

  # Run
  ansible-playbook -i inventory playbook.yml
  ```
- **Project:** You already have this! (NetOps-Automation project)
  - Just add to resume
  - Practice running it

---

### Week 11-12: Monitoring (Prometheus + Grafana)

**Prometheus & Grafana**
- **Goal:** Monitor applications and infrastructure
- **Time:** 15-20 hours
- **Resources:**
  - FREE: [Prometheus Docs](https://prometheus.io/docs/introduction/overview/)
  - FREE: [Grafana Tutorial](https://grafana.com/tutorials/)
  - FREE: [Monitoring Course (YouTube)](https://www.youtube.com/watch?v=h4Sl21AKiDg)
- **What to Learn:**
  - Prometheus metrics
  - PromQL (query language)
  - Exporters (node_exporter, etc.)
  - Grafana dashboards
  - Alerting
- **Hands-On:**
  ```yaml
  # docker-compose.yml
  version: '3'
  services:
    prometheus:
      image: prom/prometheus
      ports:
        - "9090:9090"
      volumes:
        - ./prometheus.yml:/etc/prometheus/prometheus.yml

    grafana:
      image: grafana/grafana
      ports:
        - "3000:3000"

  # Start
  docker-compose up -d

  # Access:
  # Prometheus: http://localhost:9090
  # Grafana: http://localhost:3000
  ```
- **Project:** Add monitoring to your EdgeNet-Demo
  - Prometheus to collect metrics
  - Grafana dashboard
  - Add screenshots to resume!

---

## 🎯 After 12 Weeks, You'll Have:

### Skills:
✅ Docker (hands-on)
✅ AWS (EC2, VPC, S3, Lambda)
✅ Terraform (infrastructure as code)
✅ Kubernetes (basics)
✅ CI/CD (Jenkins or GitLab CI)
✅ Ansible (configuration management)
✅ Prometheus + Grafana (monitoring)
✅ Git (version control)

### Projects to Show:
1. **EdgeNet-Demo** - Deployed on AWS with Docker
2. **NetOps-Automation** - Ansible playbooks
3. **5G-Core-Automation** - Docker Compose setup
4. **Infrastructure-as-Code** - Terraform for AWS
5. **CI/CD Pipeline** - Automated deployment

### Resume:
✅ Can list all these skills honestly
✅ Have GitHub projects to prove it
✅ Can discuss in interviews

---

## 💰 Cost Breakdown (Keep it Affordable)

### Free:
- Git tutorials
- Docker tutorials
- AWS Free Tier (12 months)
- Kubernetes (Minikube free)
- All official documentation

### Low Cost:
- Udemy courses: $15 each × 5 courses = $75
- Total: **~$75**

### Optional (High Value):
- AWS Solutions Architect cert: $150
- CKA cert: $395
- A Cloud Guru subscription: $35/month × 3 months = $105
- Total with certs: **~$650**

**My Recommendation:** Start with free resources, buy Udemy courses on sale ($10-15), consider AWS cert after 2-3 months of practice.

---

## 📅 Realistic Timeline Options

### Option 1: Aggressive (Full-time study)
- **Time:** 12 weeks (3 months)
- **Hours/week:** 30-40 hours
- **For:** If you're unemployed or can dedicate full time

### Option 2: Balanced (Part-time after work)
- **Time:** 24 weeks (6 months)
- **Hours/week:** 15-20 hours
- **For:** Currently employed, studying evenings/weekends

### Option 3: Comfortable (Steady pace)
- **Time:** 36 weeks (9 months)
- **Hours/week:** 10-12 hours
- **For:** Busy schedule, want less pressure

**My Recommendation for You:** Option 2 (6 months) - Study 2 hours/day weekdays, 5 hours each weekend day.

---

## 🎓 Free Learning Resources (Bookmark These!)

### General:
- [freeCodeCamp YouTube](https://www.youtube.com/c/Freecodecamp) - Full courses
- [AWS Skill Builder](https://skillbuilder.aws/) - Official AWS training
- [Kubernetes Official](https://kubernetes.io/docs/tutorials/) - K8s tutorials
- [Terraform Learn](https://learn.hashicorp.com/) - Official tutorials

### YouTube Channels:
- **TechWorld with Nana** - DevOps tutorials
- **NetworkChuck** - IT/Networking
- **KodeKloud** - DevOps training
- **Mumshad Mannambeth** - Kubernetes

### Practice Platforms:
- [Katacoda](https://www.katacoda.com/) - Interactive scenarios
- [Play with Docker](https://labs.play-with-docker.com/) - Free Docker playground
- [Play with Kubernetes](https://labs.play-with-k8s.com/) - Free K8s playground

---

## 🏆 Study Tips for Success

### 1. **Hands-On is CRITICAL**
- Don't just watch videos
- Type every command yourself
- Break things and fix them
- Build real projects

### 2. **Document Everything**
- Keep notes in GitHub
- Write README files
- Take screenshots
- Blog about learnings (optional but great)

### 3. **Join Communities**
- Reddit: r/devops, r/aws, r/kubernetes
- Discord: DevOps/Cloud communities
- LinkedIn: Follow hashtags #DevOps #AWS

### 4. **Study Plan**
```
Monday-Friday:
  Morning: 1 hour before work (reading)
  Evening: 2 hours after work (hands-on)

Saturday:
  Morning: 3 hours (video courses)
  Afternoon: 2 hours (hands-on projects)

Sunday:
  Morning: 2 hours (practice)
  Evening: 1 hour (review week, plan next week)

Total: 20 hours/week
```

### 5. **Track Progress**
- Use a checklist (print this guide!)
- Celebrate small wins
- Share progress on LinkedIn
- Update resume every 2 weeks

---

## ✅ Week-by-Week Checklist

### Month 1:
- [ ] Week 1: Git basics + Docker fundamentals
- [ ] Week 2: Docker Compose + Dockerize first app
- [ ] Week 3: AWS account + EC2 + VPC basics
- [ ] Week 4: S3, Lambda, deploy first app on AWS

### Month 2:
- [ ] Week 5: Terraform basics + first infrastructure
- [ ] Week 6: Terraform modules + recreate AWS infra
- [ ] Week 7: Kubernetes setup + first pod
- [ ] Week 8: K8s deployments + services

### Month 3:
- [ ] Week 9: CI/CD pipeline (Jenkins/GitLab CI)
- [ ] Week 10: Ansible playbooks
- [ ] Week 11: Prometheus + Grafana
- [ ] Week 12: Polish projects, update resume, apply for jobs!

---

## 🚀 After Learning: What to Do

### 1. Update Resume
- Add all learned skills
- List projects with GitHub links
- Quantify: "Deployed X apps using Docker" "Managed Y AWS resources with Terraform"

### 2. Update LinkedIn
- Add skills (get endorsements)
- Post about learnings
- Share projects

### 3. Build Portfolio
- GitHub profile README
- List all projects
- Add badges (AWS certified, etc.)

### 4. Start Applying
- Don't wait for perfection
- Apply with 70% match
- Practice interviews

### 5. Keep Learning
- Stay updated
- Try new tools
- Contribute to open source

---

## 💡 Final Tips

**Don't Get Overwhelmed:**
- You don't need to be expert in everything
- Basic competency in 5-6 tools is enough
- Interviewers understand you're learning

**Leverage Your Experience:**
- You have 12 years telecom experience
- You understand networks deeply
- You know automation (from Nokia)
- Cloud is just another platform

**You're NOT Starting from Zero:**
- You know Python ✅
- You know networking ✅
- You know Git ✅
- You understand systems ✅
- You just need cloud tools!

**Be Honest in Interviews:**
- "I have 6 months hands-on with AWS"
- "I built X projects with Docker"
- "I'm actively learning Kubernetes"
- "I come from telecom, bringing deep networking knowledge"

---

## 🎯 Action Plan for TODAY

**Right Now (Next 2 Hours):**
1. [ ] Create AWS Free Tier account
2. [ ] Install Docker Desktop
3. [ ] Download one Udemy course (wait for sale, $10-15)
4. [ ] Star this guide in your GitHub
5. [ ] Schedule: Block 2 hours/day in calendar for next 90 days

**This Week:**
1. [ ] Complete Docker tutorial
2. [ ] Dockerize one of your projects
3. [ ] Launch first EC2 instance
4. [ ] Join r/devops subreddit

**This Month:**
1. [ ] Complete AWS basics
2. [ ] Deploy app on AWS
3. [ ] Start Terraform
4. [ ] Update resume with "Learning: AWS, Docker, Terraform"

---

## 🏁 You Got This!

**Remember:**
- You have 12 years of experience - you're a SENIOR engineer
- You already know Python, networking, and systems
- Cloud/DevOps is just new tools, not new concepts
- Many people with less experience than you are getting these jobs
- 6 months of focused learning = job ready
- Your telecom background is VALUABLE, not a weakness

**Companies need people who understand:**
✅ Networks (you have 12 years)
✅ Automation (you do this at Nokia and Meta)
✅ Cloud (you're learning)
✅ Systems thinking (you have this)

**You're not starting over - you're adding to your existing expertise!**

Start today. One hour at a time. In 6 months, you'll be amazed at your progress.

**Let's do this! 🚀**

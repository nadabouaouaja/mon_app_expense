pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "nadabj/expense-tracker"
        DOCKER_TAG = "latest"
        KUBECONFIG = credentials('k8s') // ID du credential Jenkins contenant le fichier kubeconfig
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: ' https://github.com/nadabouaouaja/mon_app_expense.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'hh', url: '']) {
                    bat "docker push %DOCKER_IMAGE%:%DOCKER_TAG%"
                }
            }
        }

       stage('Deploy to Kubernetes') {
    steps {
        bat "dir" // debug
        bat "kubectl apply -f %WORKSPACE%\\deployment.yaml"
        bat "kubectl apply -f %WORKSPACE%\\service.yaml"
    }
}
        stage('Verify Deployment') {
            steps {
                bat 'kubectl get pods'
                bat 'kubectl get svc'
            }
        }
    }

    post {
        success {
            echo "✅ Build, Push, and Deploy succeeded!"
        }
        failure {
            echo "❌ Pipeline failed."
        }
    }
}

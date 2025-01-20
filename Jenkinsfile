pipeline {
    agent {
        label 'docker'
    }
    environment {
        APP_IMAGE = 'tpp:temp'
        SELENIUM_IMAGE = 'python'
        NETWORK_NAME = 'test_network'
        REPO_URL = 'https://github.com/dorhs/project1.git'
        BRANCH = 'main'
    }
    stages {
        stage('Clean Workspace') {
            steps {
                script {
                    cleanWs()
                    echo "Workspace cleaned."
                    // Remove all running and stopped containers
                    sh """
                    if [ \$(docker ps -a -q | wc -l) -gt 0 ]; then
                        docker rm -f \$(docker ps -a -q)
                        echo "All containers removed."
                    else
                        echo "No containers to remove."
                    fi
                    """
                    // Remove unused Docker networks
                    sh """
                    if [ \$(docker network ls | grep $NETWORK_NAME | wc -l) -eq 1 ]; then
                        docker network rm $NETWORK_NAME
                        echo "Network $NETWORK_NAME removed."
                    else
                        echo "No network named $NETWORK_NAME found."
                    fi
                    """
                    // Remove dangling Docker images
                    sh """
                    docker image prune -f
                    echo "Dangling images removed."
                    """
                }
            }
        }
        stage('Clone Repo') {
            steps {
                script {
                    git branch: BRANCH, url: REPO_URL
                }
            }
        }
        stage('Create Docker Network') {
            steps {
                script {
                    sh "docker network create $NETWORK_NAME"
                }
            }
        }
        stage('Docker Build App + Run App') {
            steps {
                dir('DomainMonitoringSystemv1.0.4') {
                    script {
                        sh "docker build -t $APP_IMAGE ."
                        sh "docker run --network host --name web_app -p 8081:8081 -d $APP_IMAGE"
                    }
                }
            }
        }
        stage('Run Selenium Container + Test the app') {
            steps {
                script {
                    sh """
                    docker build -t sel:temp .
                    docker run --network host --name selenium_test sel:temp
                    """
                }
            }
        }
        stage('Push image to docker hub') {
            environment {
                DOCKER_HUB_CREDS = credentials('docker-hub-credentials')
                DOCKER_HUB_USERNAME = 'dengol'
                DOCKER_HUB_REPO = 'dengol/tpp-app'
                GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
            }
            steps {
                script {
                    sh """
                    echo \${DOCKER_HUB_CREDS_PSW} | docker login -u \${DOCKER_HUB_CREDS_USR} --password-stdin
                    docker tag ${APP_IMAGE} ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_REPO}:\${GIT_COMMIT_SHORT}
                    docker push ${DOCKER_HUB_USERNAME}/${DOCKER_HUB_REPO}:\${GIT_COMMIT_SHORT}
                    docker logout
                    """
                }
            }
        }
    }
    post {
        always {
            script {
                // Cleanup containers, networks, and dangling images
                sh """
                docker rm -f \$(docker ps -a -q) || true
                docker network rm $NETWORK_NAME || true
                docker image prune -f || true
                """
                echo "Post-cleanup complete."
            }
        }
        failure {
            echo "Pipeline failed!"
        }
        success {
            echo "Pipeline succeeded!"
        }
    }
}

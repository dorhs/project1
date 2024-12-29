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
                        sh "docker run --network $NETWORK_NAME --name web_app -p 8081:8081 -d $APP_IMAGE"
                    }
                }
            }
        }

        stage('Run Selenium Container') {
            steps {
                script {
                    sh """
                    sudo docker run --network host --name selenium_test $SELENIUM_IMAGE
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

pipeline {
    agent {
        label 'docker'
    }

    environment {
        APP_IMAGE = 'tpp:temp'
        SELENIUM_IMAGE = 'selenium:selenium'
        NETWORK_NAME = 'test_network'
        REPO_URL = 'https://github.com/dorhs/project1.git'
        BRANCH = 'main'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                script {
                    // Clean Jenkins workspace
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
                    if [ \$(docker images -f "dangling=true" -q | wc -l) -gt 0 ]; then
                        docker rmi \$(docker images -f "dangling=true" -q)
                        echo "Dangling images removed."
                    else
                        echo "No dangling images to remove."
                    fi
                    """

                    // Remove unused Docker volumes
                    sh """
                    if [ \$(docker volume ls -q | wc -l) -gt 0 ]; then
                        docker volume rm \$(docker volume ls -q)
                        echo "Unused volumes removed."
                    else
                        echo "No unused volumes to remove."
                    fi
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

        stage('Docker Build App') {
            steps {
                dir('DomainMonitoringSystemv1.0.4') {
                    script {
                        sh "docker build -t $APP_IMAGE ."
                    }
                }
            }
        }

        stage('Run Web App Container') {
            steps {
                script {
                    sh """
                    docker run --network $NETWORK_NAME --name web_app -p 8081:8081 -d $APP_IMAGE
                    """
                }
            }
        }

        stage('Docker Build Selenium') {
            steps {
                script {
                    sh "docker build -t $SELENIUM_IMAGE ."
                }
            }
        }

        stage('Run Selenium Container') {
            steps {
                script {
                    sh """
                    docker run --network $NETWORK_NAME --name selenium_test -d $SELENIUM_IMAGE
                    docker logs -f selenium_test
                    """
                }
            }
        }
    }

    post {
        always {
            script {
                // Clean up after pipeline
                sh """
                docker rm -f \$(docker ps -a -q) || true
                docker network rm $NETWORK_NAME || true
                docker rmi -f $APP_IMAGE $SELENIUM_IMAGE || true
                docker volume rm \$(docker volume ls -q) || true
                """
                echo "Pipeline cleanup complete."
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

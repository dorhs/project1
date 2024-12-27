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
                    cleanWs()
                    echo "Workspace cleaned."

                    sh """
                    if [ \$(docker ps -a -q | wc -l) -gt 0 ]; then
                        docker rm -f \$(docker ps -a -q)
                    else
                        echo "No containers to remove."
                    fi
                    if [ \$(docker network ls | grep $NETWORK_NAME | wc -l) -eq 1 ]; then
                        docker network rm $NETWORK_NAME
                    fi
                    """
                }
                echo "Docker containers and networks cleaned."
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
            echo "Pipeline completed."
        }
        failure {
            echo "Pipeline failed!"
        }
        success {
            echo "Pipeline succeeded!"
        }
    }
}

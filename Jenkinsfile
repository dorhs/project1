pipeline {
    agent {
        label 'docker'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                script {
                    cleanWs()
                    echo "Workspace cleaned."
                    sh """
                    if [ \$(sudo docker ps -a -q | wc -l) -gt 0 ]; then
                    sudo docker rm -f \$(sudo docker ps -a -q)
                    else
                    echo "No containers to remove."
                    fi
                    """

                }
                echo "Docker containers removed."
            }
        }

        stage('Clone Repo') {
            steps {
                script {
                    git branch: 'main', url: 'https://github.com/dorhs/project1.git'
                }
            }
        }

        stage('Docker Build appTPP') {
            steps {
                dir('DomainMonitoringSystemv1.0.4') {
                    script {
                        sh """
                        sudo docker build -t tpp:temp .
                        """
                    }
                }
            }
        }

        stage('Run Container TPP') {
            steps {
                script {
                    sh """
                    sudo docker run -p 8081:8081 -d tpp:temp
                    """
                }
            }
        }
    }
    
        stage('Docker Build Selenium') {
          steps {
               dir('/') {
                   script {
                       sh """
                       sudo docker build -t selenium:selenium .
                       """
                    }
                }
            }
        }

        stage('Run Container Selenium') {
            steps {
                script {
                    sh """
                    sudo docker run -p 8082:8082 -d selenium:selenium
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed!"
        }
        success {
            echo "Pipeline succeeded!"
      }
  }


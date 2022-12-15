pipeline {
    agent any
    environment {
      PROJECT_ID = 'oss-20190928'
      CLUSTER_NAME = 'kube-20190928'
      LOCATION = 'asia-northeast3-a'
      CREDENTIALS_ID = 'gke'
    }
    stages {
        stage("Checkout code") {
            steps {
                checkout scm
            }
        }
        stage("Build image") {
            steps {
                script {
                    myapp = docker.build("daeunnniii/miraclenote:${env.BUILD_ID}")
                }
            }
        }
        stage("Push image") {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                            myapp.push("latest")
                            myapp.push("${env.BUILD_ID}")
                    }
                }
            }
        }        
        stage('Deploy Kubernetes') {
			when {
				branch 'master'
			}
          steps{
            sh "sed -i 's/miraclenote:latest/miraclenote:${env.BUILD_ID}/g' manifests/manifests.yaml"
            step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, 
              clusterName: env.CLUSTER_NAME, location: env.LOCATION, 
              manifestPattern: 'manifests/manifests.yaml', credentialsId: env.CREDENTIALS_ID, 
              verifyDeployments: true])
          }
        }
    }    
}

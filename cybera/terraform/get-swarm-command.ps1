$swarm_token = $(ssh -i "C:\\Users\\rova\\.ssh\\cybera" -o StrictHostKeyChecking=no -o LogLevel=quiet ubuntu@10.2.9.11 'sudo docker swarm join-token manager') | Out-String
Write-Output $swarm_token
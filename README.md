# coverity

This place will help you to play with all the fancy functionalies such as Jenkins, JIRA, Web API, and E-mail notification.

1. Jenkins Integration

- Setup for Jenkins
	- Setup Jenkins user to the same as Coverity user at /etc/default/jenkins
	- Change Jenkins file owner to Coverity user e.g.
		chown yuan:yuan /var/lib/jenkins
		chown yuan:yuan /var/cache/jenkins
		chown yuan:yuan /var/log/jenkins
	- restart Jenkins
		sudo service restart jenkins
- Create project in Jenkins
- Run run.sh in Jenkins to initiate Coverity configure/build/analyze/commit

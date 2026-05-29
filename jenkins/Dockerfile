FROM jenkins/jenkins:lts

# Mude para user root para instalar plugins
USER root

# Desabilita o wizard de setup inicial
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Copie a lista de plugins
COPY jenkins/plugins.txt /usr/share/jenkins/ref/plugins.txt

# Instale os plugins
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

# Copie a configuração JCasC
COPY jenkins/casc.yaml /var/jenkins_home/casc.yaml

# Crie o diretório de scripts Groovy
RUN mkdir -p /var/jenkins_home/init.groovy.d/

# Copie os scripts de inicialização Groovy
COPY jenkins/init.groovy.d/ /var/jenkins_home/init.groovy.d/

# Configure permissões
RUN chown -R jenkins:jenkins /var/jenkins_home/

# Configure a variável de ambiente para JCasC
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc.yaml

# Volte para o usuário jenkins
USER jenkins

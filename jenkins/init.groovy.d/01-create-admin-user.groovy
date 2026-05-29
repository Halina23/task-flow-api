import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import jenkins.install.InstallState

def jenkins = Jenkins.getInstance()

try {
    // Desabilita o wizard de setup inicial
    InstallState.getInstance().setNewInstance(false)
    
    // Setup security realm - APENAS se não estiver já configurado
    if (!(jenkins.getSecurityRealm() instanceof HudsonPrivateSecurityRealm)) {
        println("✓ Configurando segurança local...")
        def realm = new HudsonPrivateSecurityRealm(false, false)
        jenkins.setSecurityRealm(realm)
    }
    
    // Define admin username e password
    def adminUser = System.getenv("JENKINS_ADMIN_ID") ?: "admin"
    def adminPassword = System.getenv("JENKINS_ADMIN_PASSWORD") ?: "admin123"
    
    // Cria ou atualiza o usuário admin
    def realm = jenkins.getSecurityRealm()
    def user = realm.getUser(adminUser)
    
    if (user == null) {
        println("✓ Criando usuário admin: ${adminUser}")
        user = realm.createAccount(adminUser, adminPassword)
        user.save()
    } else {
        println("✓ Usuário admin já existe: ${adminUser}")
    }
    
    // Setup authorization
    jenkins.setAuthorizationStrategy(new FullControlOnceLoggedInAuthorizationStrategy())
    
    // Salva todas as configurações
    jenkins.save()
    
    println("✓ Jenkins inicializado com sucesso!")
    println("✓ Acesse em: http://localhost:8081/")
    
} catch (Exception e) {
    println("✗ Erro durante inicialização do Jenkins: ${e.message}")
    e.printStackTrace()
}
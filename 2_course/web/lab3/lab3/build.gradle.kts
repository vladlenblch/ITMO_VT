plugins {
    java
    war
}

group = "org.example"
version = "1.0-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

repositories {
    mavenCentral()
}

val primefacesVersion = "14.0.0"
val postgresqlVersion = "42.7.7"

dependencies {
    implementation("org.postgresql:postgresql:$postgresqlVersion")
    
    implementation("org.primefaces:primefaces:13.0.4:jakarta")
    
    compileOnly("jakarta.platform:jakarta.jakartaee-web-api:9.1.0")
    
    implementation("org.glassfish:jakarta.faces:3.0.2")
    
    compileOnly("jakarta.servlet:jakarta.servlet-api:5.0.0")
    
    implementation("jakarta.persistence:jakarta.persistence-api:3.0.0")
    
    implementation("org.glassfish:jakarta.el:4.0.2")
    
    implementation("jakarta.validation:jakarta.validation-api:3.0.0")
    implementation("org.hibernate.validator:hibernate-validator:7.0.5.Final")
    
    compileOnly("jakarta.enterprise:jakarta.enterprise.cdi-api:3.0.0")
    
    implementation("jakarta.interceptor:jakarta.interceptor-api:2.1.0")
    
    implementation("jakarta.servlet.jsp.jstl:jakarta.servlet.jsp.jstl-api:2.0.0")
    implementation("org.glassfish.web:jakarta.servlet.jsp.jstl:2.0.0")
}

tasks.war {
    archiveFileName.set("lab3.war")
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    
    exclude("META-INF/versions/9/module-info.class")
    exclude("**/javax/**")
    exclude("**/META-INF/services/javax.*")
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
    options.compilerArgs.add("-parameters")
}
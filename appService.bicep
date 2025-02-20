param webAppName string = 'weather-flask-app-${uniqueString(resourceGroup().id)}' 
param sku string = 'F1' // Free Tier (F1)
param linuxFxVersion string = 'python|3.10' 
param location string = resourceGroup().location 
param repositoryUrl string = 'https://github.com/MariosGramm/WeatherMonitoringApp' 
param branch string = 'main' 


var appServicePlanName = toLower('AppServicePlan-${webAppName}')
var webSiteName = toLower('flaskapp-${webAppName}')

resource appServicePlan 'Microsoft.Web/serverfarms@2020-06-01' = {
  name: appServicePlanName
  location: location
  properties: {
    reserved: true
  }
  sku: {
    name: sku
    tier: 'Free'
  }
  kind: 'linux'
}

resource appService 'Microsoft.Web/sites@2020-06-01' = {
  name: webSiteName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
    }
  }
}

resource srcControls 'Microsoft.Web/sites/sourcecontrols@2021-01-01' = {
  parent: appService 
  name: 'web'       
  properties: {
    repoUrl: repositoryUrl
    branch: branch
    isManualIntegration: false // Automatic Integration 
    deploymentRollbackEnabled: true 
  }
}

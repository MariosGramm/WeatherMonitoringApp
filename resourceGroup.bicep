targetScope='subscription'


resource ResGroup 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'AppServiceRG'
  location: 'westeurope'
}

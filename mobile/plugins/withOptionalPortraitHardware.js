const { withAndroidManifest } = require('expo/config-plugins');

module.exports = function withOptionalPortraitHardware(config) {
  return withAndroidManifest(config, (config) => {
    const manifest = config.modResults.manifest;
    const name = 'android.hardware.screen.portrait';
    manifest['uses-feature'] = (manifest['uses-feature'] || []).filter(
      (feature) => feature.$?.['android:name'] !== name,
    );
    manifest['uses-feature'].push({
      $: { 'android:name': name, 'android:required': 'false' },
    });
    return config;
  });
};

const postcssPresetEnv = require("postcss-preset-env");

module.exports = {
  plugins: [
    require('postcss-import'),
    require('tailwindcss/nesting')(require('postcss-nesting')),
    require('tailwindcss'),
    require('postcss-preset-env')({
      features: {'nesting-rules': false }
    }),
    require('autoprefixer'), 
    require('cssnano')({
      preset: 'default'
    }),
  ]
};

module.exports = {
  env: {
      browser: true,
      es6: true,
      node: true,
  },
  parserOptions: {
      sourceType: 'module',
      ecmaVersion: 2017
  },
  extends: 'eslint:recommended',
  globals: {
      $: 'readonly',
      jQuery: 'readonly'
  },
  rules: {

  },
};
// vue.config.js
module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // vagy a Flask szerverd címe és portja
        changeOrigin: true,
        pathRewrite: {
          '^/api': '', // Lehet, hogy nem kell a pathRewrite, ha nincs prefix
        },
      },
    },
  },
};

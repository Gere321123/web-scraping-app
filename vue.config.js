module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // vagy 'http://localhost:5000'
        changeOrigin: true,
        pathRewrite: {
          '^/api': '', // Így töröld le az '/api' prefixet, ha a Flask szerver nem várja el
        },
      },
    },
  },
};

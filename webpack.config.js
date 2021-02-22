const path = require('path');

module.exports = {
    mode: "development",
    //entry: path.resolve(__dirname, '/annotation_tool/frontend/src/index.js'),
    entry:  ['babel-polyfill',path.resolve('/home/alex/PycharmProjects/django_jwt_react/django_jwt_react/annotation_tool/frontend/src/index.js')],
    output: {
        // options related to how webpack emits results

        // where compiled files go
        path: path.resolve( "/home/alex/PycharmProjects/django_jwt_react/django_jwt_react/annotation_tool/frontend/static/frontend/public/"),

        // 127.0.0.1/static/frontend/public/ where files are served from
        publicPath: "/static/frontend/public/",
        filename: 'main.js',  // the same one we import in index.html
    },
    module: {
        // configuration regarding modules
        rules: [
            {
                // regex test for js and jsx files
                test: /\.(js|jsx)?$/,
                // don't look in the node_modules/ folder
                exclude: /node_modules/,
                // for matching files, use the babel-loader
                use: {
                    loader: "babel-loader",
                    options: {presets: ["@babel/env"]}
                },
            },
           {
        test: /\.less$/i,
        loader: "less-loader", // compiles Less to CSS
      },
        {
         test: /\.css$/i,
        use: [ "css-loader"]
      },



        ],
    },
};
'use strict';
var fs = require('fs');
var path = require('path');
var autoprefixer = require('autoprefixer');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var _ = require('lodash');

var scssDir = './static/scss/';
var jsxDir = './static/jsx/';


// Attempt to delete the file, but don't throw an error if it's missing.
function tryUnlink(path) {
  try {
    fs.unlinkSync(path);
  } catch (err) {
    // If error is not file missing, throw the error again.
    if (err.code !== 'ENOENT') {
      throw err;
    }
    console.log('Unable to delete file:', path);
  }
}


/*
 * This is a modified version webpack-bundle-tracker. The original:
 * https://github.com/owais/webpack-bundle-tracker/tree/763c326bbb06ea1028d9ac5db11e7ffc91d9257e
 *
 * The original bundle-tracker would overwrite the webpack-stats.json file while
 * compiling, breaking the website during deployment. The original also did
 * not delete old files after the build finished, wasting a ton of space.
 *
 * This version only writes to webpack-stats.json once the build is complete,
 * then deletes the old bundle files.
 */
var DEFAULT_OUTPUT_FILENAME = 'webpack-stats.json';
var DEFAULT_LOG_TIME = false;


function BundleTracker(options) {
  this.options = options || {};
  this.options.filename = this.options.filename || DEFAULT_OUTPUT_FILENAME;
  if (this.options.logTime === undefined) {
    this.options.logTime = DEFAULT_LOG_TIME;
  }
}

BundleTracker.prototype.apply = function (compiler) {
  var self = this;

  // Once compiler has finished the new bundle json object will be created and
  // written. New paths of these bundles will be pushed in order to compare the
  // previous versions of the bundles.
  compiler.plugin('done', function (stats) {
    if (stats.compilation.errors.length > 0) {
      var error = stats.compilation.errors[0];
      self.writeOutput(compiler, {
        status: 'error',
        error: error['name'],
        message: error['message']
      });
      return;
    }

    var chunks = {};
    var newPaths = [];
    stats.compilation.chunks.map(function (chunk) {
      var files = chunk.files.map(function (file) {
        var F = {name: file};
        if (compiler.options.output.publicPath) {
          F.publicPath = compiler.options.output.publicPath + file;
        }
        if (compiler.options.output.path) {
          F.path = path.join(compiler.options.output.path, file);
          newPaths.push(F.path);
        }
        return F;
      });
      chunks[chunk.name] = files;
    });
    var output = {
      status: 'done',
      chunks: chunks
    };

    if (self.options.logTime === true) {
      output.startTime = stats.startTime,
        output.endTime = stats.endTime
    }

    self.writeOutput(compiler, output, newPaths);
  });
};


BundleTracker.prototype.writeOutput = function (compiler, contents, newPaths) {
  var outputDir = this.options.path || '.';
  var outputFilename = path.join(outputDir, this.options.filename || DEFAULT_OUTPUT_FILENAME);
  if (compiler.options.output.publicPath) {
    contents.publicPath = compiler.options.output.publicPath
  }

  var oldStats = null;
  if (fs.existsSync(outputFilename)) {
    oldStats = JSON.parse(fs.readFileSync(outputFilename, 'utf8'));
  }

  fs.writeFileSync(outputFilename, JSON.stringify(contents));

  // Delete old bundles after the new webpack-stats.json has been written.
  if (oldStats) {
    var isInNewPaths = function (path) {
      return _.includes(newPaths, path);
    };

    var paths = _(oldStats.chunks).values()
      .flatten()
      .pluck('path')
      .reject(isInNewPaths)
      .value();

    paths.forEach(tryUnlink);
  }
};


var baseConfig = {
  evtool: "source-map",
  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules|static\/vendor/,
        loader: 'babel-loader',
        query: {
          "presets": ["es2015", "react"]
        }
      },
      {
        id: 'sass-loader-config',
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract('style', 'css?sourceMap!postcss!sass?sourceMap')
      }
    ]
  },
  entry: {
    app_style: scssDir + 'global.scss',
    date_picker: scssDir + '/components/datepicker.scss',
    profile: jsxDir + 'Profile.jsx',
    home: jsxDir + 'Home.jsx',
    find_friends: jsxDir + 'FindFriends.jsx',
    create_event: jsxDir + 'CreateEvent.jsx',
  },
  output: {
    path: path.join(__dirname, 'static/dist'),
    filename: '[name].bundle.js'
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new ExtractTextPlugin('[name].css')
  ],
  postcss: [
    autoprefixer({browsers: ['> 3%', 'last 2 versions']})
  ],
  resolve: {
    extensions: ['', '.js', '.jsx'],
  }
};

//var sassLoader = _.findWhere(baseConfig.module.loaders, { id: 'sass-loader-config' });
//sassLoader.loader = ExtractTextPlugin.extract('style', 'css?minimize!postcss!sass');
module.exports = baseConfig;
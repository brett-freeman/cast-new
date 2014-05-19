"use strict";angular.module("doowb.angular-pusher",[]).provider("PusherService",function(){function createScript($document,protocol,callback){var tag=$document.createElement("script");tag.type="text/javascript",tag.async=!0,tag.id=scriptId,tag.src="https"==protocol?secureScriptUrl:scriptUrl,tag.onreadystatechange=tag.onload=function(){var state=tag.readState;callback.done||state&&!/loaded|complete/.test(state)||(callback.done=!0,callback())},$document.getElementsByTagName("head")[0].appendChild(tag)}var scriptUrl="//js.pusher.com/2.1/pusher.min.js",secureScriptUrl="//d3dy5gmtp8yhk7.cloudfront.net/2.1/pusher.min.js",scriptId="pusher-sdk",apiKey="",initOptions={};this.setPusherUrl=function(url){return url&&(scriptUrl=secureScriptUrl=url),this},this.setOptions=function(options){return initOptions=options||initOptions,this},this.setToken=function(token){return apiKey=token||apiKey,this},this.$get=["$document","$timeout","$q","$rootScope","$window","$location",function($document,$timeout,$q,$rootScope,$window,$location){function onSuccess(){pusher=new $window.Pusher(apiKey,initOptions)}var pusher,deferred=$q.defer(),protocol=$location.protocol(),onScriptLoad=function(){onSuccess(),$timeout(function(){deferred.resolve(pusher)})};return createScript($document[0],protocol,onScriptLoad),deferred.promise}]}).factory("Pusher",["$rootScope","PusherService",function($rootScope,PusherService){return{subscribe:function(channelName,eventName,callback){PusherService.then(function(pusher){var channel=pusher.channel(channelName)||pusher.subscribe(channelName);channel.bind(eventName,function(data){callback&&callback(data),$rootScope.$broadcast(channelName+":"+eventName,data),$rootScope.$digest()})})},unsubscribe:function(channelName){PusherService.then(function(pusher){pusher.unsubscribe(channelName)})}}}]);
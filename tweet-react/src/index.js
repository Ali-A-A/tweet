import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { TweetsComponent , TweetDetail } from './tweets/components';


const tweetEl = document.getElementById("root");
ReactDOM.render(
   <TweetsComponent username={tweetEl.dataset.username} canTweet={tweetEl.dataset.canTweet} />,
  tweetEl
);
const TweetDetailEl = document.querySelectorAll(".tweet-detail")

TweetDetailEl.forEach(container => {
  ReactDOM.render(
    <TweetDetail tweetId={container.dataset.tweetId} className={container.dataset.className} />,
   container
 );
})

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

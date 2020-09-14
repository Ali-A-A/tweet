import React, { useState, useEffect, Fragment } from 'react'
import { loadTweets , handleDidLike , createTweet } from '../lookup/components'





export const TweetList = (props) => {
    const [tweets , setTweets] = useState([])
    const [tweets2 , setTweets2] = useState([])
    useEffect(() => {
        let final = [...props.newTweets].concat(tweets)
        if (final.length !== tweets2.length) {
            setTweets2(final)
        }
    } , [props.newTweets , tweets , tweets2])
    useEffect(() => {
        loadTweets(setTweets)
    } , [])

    return (
        <div className="App">
        {tweets2.map(((tweet) => {
            return <Tweet tweet={tweet} setTweets={setTweets} key={tweet.id} />
        }))}
    </div>
    )
}

export const Btns = (props) => {
    const {tweet} = props
    const [likes , setLikes] = useState(tweet.likes ? tweet.likes : 0)
    const handleAction = (res , stat) => {
        if(stat === 200)
            setLikes(JSON.parse(res).likes)
        else
            alert("Error in like")
    }
    return (
        <Fragment>
            <div className='text-danger m-3'><p>Likes : {likes}</p></div>
            <button className="btn btn-success ml-2" onClick={() => handleDidLike(tweet.id , handleAction , tweet.content ,  'like')}>Like</button>
            <button className="btn btn-danger ml-2" onClick={() => handleDidLike(tweet.id , handleAction , tweet.content ,  'unlike')}>Un Like</button>
        </Fragment>
    )
}

export const ReTweetBtn = (props) => {
    const {tweet , setTweets} = props
    return <button className="btn btn-info m-2" onClick={() => handleDidLike(tweet.id , setTweets , tweet.content , 'retweet')}>Re Tweet</button>
}


export const Tweet = props => {
    const {tweet , setTweets} = props
    return (
    <div style={{display: "inline-block"}} className='rounded m-3 col-12 col-md-5 col-lg-3 border bg-dark' id={"tweet-" + tweet.id}>
      <h3 className='text-success'>Tweet {tweet.id}</h3>
      <div className='text-info m-3'><p>{tweet.content ? tweet.content : 'NO CONTENT'}</p></div>
      <Btns tweet={tweet} />
      <ReTweetBtn tweet={tweet} setTweets={setTweets} />
    </div>)
}

export const TweetsComponent = (props) => {
    const textRef = React.createRef()
    const [newTweets , setNewTweets] = useState([])
    const handleSubmit = (e) => {
        e.preventDefault()
        const newVal = textRef.current.value
        var tempNewTweets = [...newTweets]
        createTweet(newVal , (res , stat) => {
            if(stat === 201) {
                tempNewTweets.unshift(JSON.parse(res))
                setNewTweets(tempNewTweets)
            }
            else {
                alert("error in create")
            }
        })
        textRef.current.value = ''
    }
    return (
        <div className={props.className}>
            <div className="m-3">
                <form onSubmit={handleSubmit} className="col-6 offset-3">
                <div className="justify-content-center">
                    <textarea ref={textRef} className="form-control" name="tweet">

                    </textarea>
                    <button type='submit' className="btn btn-primary my-3">Tweet</button>
                </div>
                </form>
            </div>
            <TweetList newTweets={newTweets}/>
        </div>
    )
}
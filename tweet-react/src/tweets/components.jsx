import React, { useState, useEffect, Fragment } from 'react'
import { loadTweets , handleDidLike , createTweet } from '../lookup/components'



export const TweetList = (props) => {
    const {username} = props
    const [tweets , setTweets] = useState([])
    const [tweets2 , setTweets2] = useState([])
    useEffect(() => {
        let final = [...props.newTweets].concat(tweets)
        if (final.length !== tweets2.length) {
            setTweets2(final)
        }
    } , [props.newTweets , tweets , tweets2])
    useEffect(() => {
        loadTweets(setTweets , username)
    } , [username])

    return (
        <div className="App">
        {tweets2.map(((tweet) => {
            return <Tweet tweet={tweet} setTweets={props.reTweetCallback} className='rounded m-3 col-10 border bg-dark' key={tweet.id} />
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

const ParentTweet = (props) => {
    const {tweet , setTweets} = props
    return (
        <Fragment>
        {tweet.parent && <h3 className="text-success mt-3">Retweet of :</h3>}
            <div>
                <p>{tweet.parent && <Tweet tweet={tweet.parent} setTweets={setTweets} className='rounded m-3 col-10 border bg-warning' />}</p>
            </div>
        </Fragment>
    )
}


export const Tweet = props => {
    const {tweet , setTweets , className} = props
    return (
    <div style={{display: "inline-block"}} className={className} id={"tweet-" + tweet.id}>
        <h3 className='text-success'>Tweet {tweet.id}</h3>
        <ParentTweet tweet={tweet} setTweets={setTweets} />
        <div className='text-info m-3'><p>{tweet.content ? tweet.content : 'NO CONTENT'}</p></div>
        {className === 'rounded m-3 col-10 border bg-warning' ? null : <Fragment><Btns tweet={tweet} /><ReTweetBtn tweet={tweet} setTweets={setTweets} /></Fragment>}
    </div>)
}

export const TweetsComponent = (props) => {
    const {username} = props
    const canTweet = props.canTweet === "false" ? false : true
    const textRef = React.createRef()
    const [newTweets , setNewTweets] = useState([])

    const reTweetCallback = (res , stat) => {
        var tempRetweet = [...newTweets]
        if(stat === 201) {
            tempRetweet.unshift(JSON.parse(res))
            setNewTweets(tempRetweet)
        } else {
            alert("error in retweet")
        }
    }
    const handleSubmit = (e) => {
        e.preventDefault()
        const newVal = textRef.current.value
        if(newVal.trim() === "") {
            alert("Tweet can't be empty")
        } else {
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
        }
        textRef.current.value = ''
    }
    return (
        <div className='text-center'>
            {canTweet && <div className="m-3">
                <form onSubmit={handleSubmit} className="col-6 offset-3">
                <div className="justify-content-center">
                    <textarea ref={textRef} className="form-control" name="tweet">

                    </textarea>
                    <button type='submit' className="btn btn-primary my-3">Tweet</button>
                </div>
                </form>
            </div>}
            <TweetList newTweets={newTweets} reTweetCallback={reTweetCallback} username={username} />
        </div>
    )
}
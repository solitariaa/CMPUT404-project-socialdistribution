import { post, get, put, del } from "./requests";

export function getInbox(authorID) {
    return get("authors/" + authorID + "inbox/");
}

export function createPost(data, userID){
    console.log(userID + "posts/");
    return post(userID + "posts/", data);
}

export function editPost(data, postID){
    return put(postID, data);
}

export function deletePost(postID){
    return del(postID);
}

export function getUnlistedPost(url){
    const authorID = url.split("posts/")[0];
    return get("authors/" + authorID + "/posts/" + url + "/");
}

export function getPost(data, authorID, postID){
    const url = "authors/" + authorID + "/posts/" + postID + "/"
    return get(url.replaceAll("/", "%2F"), data);
}


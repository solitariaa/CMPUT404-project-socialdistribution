import { post, get, del, patch } from "./requests";


export function createComment(postData, commentData){
    console.log(postData.id);
    console.log("authors/" + postData.author.id.replace(/\/$/, "") + "/inbox/")
    return post("authors/" + postData.author.id + "/inbox/", commentData);
}

export function editComment(oldComment, content){
    return patch(oldComment.id, content);
}

export function deleteComment(comment){
    return del(comment.id);
}

export function getComments(postData){
    return get("authors/" + postData.author.id + "posts/" + postData.id + "/comments/");
}


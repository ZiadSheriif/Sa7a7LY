// Import axios
import axios from "../API/axios";

/**
 * A service to handle the submission of a post
 *
 * @param {Function} dataFetch - The function to make the request
 * @param {Object} post - The post data
 */
const submitPost = (dataFetch, post) => {
  dataFetch({
    axiosInstance: axios,
    method: "post",
    url: "/api/listing/submit/",
    requestConfig: {
      data: post,
      headers: {
        "Content-Language": "en-US",
        "Content-Type": "multipart/form-data",
      },
    },
  });
};

export default submitPost;

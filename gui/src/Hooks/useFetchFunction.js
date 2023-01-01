// Import hooks
import { useState, useEffect } from "react";

/**
 *
 * @returns {Array} - Array of response, error, loading, and axiosFetch
 */
const useFetchFunction = () => {
  // The response state
  const [response, setResponse] = useState([]);
  // The error state
  const [error, setError] = useState("");
  // The loading state (used to show something like a spinner)
  const [loading, setLoading] = useState(false);
  // The reloading state (used to trigger a reload of the data)
  const [controller, setController] = useState();

  /**
   *  Used to fetch data from an API
   */
  const fetchData = async (configObj) => {
    const { axiosInstance, method, url, requestConfig = {} } = configObj;

    try {
      setLoading(true);
      const ctrl = new AbortController();
      setController(ctrl);
      const res = await axiosInstance({
        method,
        url,
        ...requestConfig,
        signal: ctrl.signal,
      });
      setResponse(res.data);
      setError(null);
    } catch (err) {
      setError(err.response.data.error ? err.response.data.error : err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // useEffect cleanup function
    return () => controller && controller.abort();
  }, [controller]);

  return [response, error, loading, fetchData];
};

export default useFetchFunction;

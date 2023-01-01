// Import themes
import lightTheme from "./Theme/lightTheme";

// Import theme provider from styled components
import { ThemeProvider } from "styled-components";
import "./App.css";
import ImagesAndVideosTab from "./Components/ImagesAndVideosTab/ImagesAndVideosTab";
import submitPost from "./Services/submitPost";
import useFetchFunction from "./Hooks/useFetchFunction";
import CheckInput from "./Components/CheckInput/CheckInput";

function App() {
  const [data, error, isLoading, dataFetch] = useFetchFunction();

  /**
   * Function to handle submit the post
   * (Called when the user clicks on the submit button)
   */
  const handleSubmit = ({ attachments = [] } = {}) => {
    var bodyFormData = new FormData();
    attachments.forEach((element) => {
      bodyFormData.append("attachments", element, element.path);
    });
    submitPost(dataFetch, bodyFormData);
  };
  return (
    <div className="App">
      <ThemeProvider theme={lightTheme}>
        <ImagesAndVideosTab
          submitPost={handleSubmit}
          isLoadingSubmit={isLoading}
        />
        <CheckInput />
      </ThemeProvider>
    </div>
  );
}

export default App;

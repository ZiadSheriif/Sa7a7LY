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
  console.log("data", data);
  /**
   * Function to handle submit the post
   * (Called when the user clicks on the submit button)
   */
  const handleSubmit = ({
    attachments = [],
    codesChoice,
    digitsChoice,
  } = {}) => {
    console.log("input", attachments);
    console.log("codesChoice", codesChoice);
    console.log("digitsChoice", digitsChoice);
    var bodyFormData = new FormData();
    attachments.forEach((element) => {
      bodyFormData.append("input", element, element.path);
    });
    bodyFormData.append("codesChoice", codesChoice);
    bodyFormData.append("digitsChoice", digitsChoice);
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

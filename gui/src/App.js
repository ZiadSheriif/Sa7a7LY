// Import themes
import lightTheme from "./Theme/lightTheme";

// Import theme provider from styled components
import { ThemeProvider } from "styled-components";
import "./App.css";
import ImagesAndVideosTab from "./Components/ImagesAndVideosTab/ImagesAndVideosTab";

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={lightTheme}>
        <ImagesAndVideosTab />
      </ThemeProvider>
    </div>
  );
}

export default App;

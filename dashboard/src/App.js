import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layout";
import Predict from "./pages/predict";
import Settings from "./pages/settings";
import NotFound from "./pages/not_found";
import "rsuite/dist/rsuite.min.css";
import "./App.css";

function App() {
  return (
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Predict />} />
            <Route path="settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </BrowserRouter>
  );
}

export default App;

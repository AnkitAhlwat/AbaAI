import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const url = `${import.meta.env.VITE_API_BASE_URL}/hello`;
      const response = await axios.get(url);
      console.log(response);
      setData(response.data);
    };

    fetchData();
  }, []);

  return (
    <>
      <div className="App">
        <p>{data.message}</p>
      </div>
    </>
  );
}

export default App;

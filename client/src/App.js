import React, {useState, useEffect} from 'react' 
import SearchElement from './components/SearchElement';
import SearchElementDescriptor from './components/SearchElementDescriptor'
import './styles/SearchInput.css'
function App()
{
    const [data, setData] = useState([]);
    const [userPrompt, setUserPrompt] = useState("");
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {

    }, [])

    const fetchPrompt = () => {
        setLoading(true);
        fetch("/prompt", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userPrompt})
        })
        .then(res => res.json())
        .then(prompt => {
            console.log("Fetched prompt:", prompt.data)
            setData(prompt.data)
            setLoading(false);
        })
        .catch(error => {
            console.error("Error fetching prompt:", error);
            setLoading(false);
        })
    };
    return (
        <div>
            <div className='SearchInput'>
            <input
                type="text"
                value={userPrompt}
                onChange={(e) => setUserPrompt(e.target.value)}
                placeholder="Wpisz swój prompt..."
            />
            <button onClick={fetchPrompt} disabled={loading}>Wyślij</button>
            </div>
            {loading ?  <div className="centered-message">Loading...</div> : data.length !== 0 ? (
            <div>
            <SearchElementDescriptor/>
            {data.map((element, index) => <SearchElement key={index} link={element[0]} accuracy={element[1]}/>)}
            </div>) :  <div className="centered-message">Not found</div>
            }
        </div>
    );
}

export default App
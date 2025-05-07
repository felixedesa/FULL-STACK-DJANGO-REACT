import { Button, Container, Grid, Image, Text, Title } from "@mantine/core"
import { useEffect, useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom";

function Profile () {

    const navigate = useNavigate();

    const [count, setCount] = useState(0)
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")

    const token = localStorage.getItem('ssgiToken');

    const handleClick = () => {
        setCount(count + 1)
    }

    useEffect(()=>{

        axios.get("http://localhost:8000/api/users/", {headers: {
            'Authorization': `Bearer ${token}`
        }},
        {withCredentials: true})
        .then(res => {
            setUsername(res.data[0].username);
            setEmail(res.data[0].email);
        })
        .catch(()=> {navigate('/login');})
    })

    return (
        <Container size={"md"} mt={"lg"}>
            <Grid>
                <Grid.Col span={4} >
                    <Image src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/images/bg-7.png"/>
                    <Title order={2} fz={"h3"} c={"gray.6"} my={"md"}>Details</Title>
                    <Text>name: {username}</Text>
                    <Text>email: {email}</Text>
                    <Title order={2} fz={"h3"} c={"gray.6"} my={"md"}>Skills</Title>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                </Grid.Col>
                <Grid.Col offset={1} span={7} >
                    <Button variant="filled" radius={"xl"} onClick={handleClick}>Button</Button>
                    <Text mt={"lg"}>{count}</Text>
                </Grid.Col>
            </Grid>
        </Container>
    )
}

export default Profile
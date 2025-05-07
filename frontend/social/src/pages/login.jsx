import { Button, Container, Grid, Image, PasswordInput, Stack, Text, TextInput, Title } from "@mantine/core"
import { useState } from "react"
import axios from "axios"

function Login () {

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const handleLogin = async () => {
        try {
            await axios.post("http://localhost:8000/api/login/",
                {email: username, password},
                {withCredentials: true})
                .then(res => localStorage.setItem("ssgiToken", res.data.access));
                alert("Logged in");

        } catch {
            alert("Login failed");
        }
    }

    return (
        <Container size={"md"} mt={"lg"}>
            <Grid>
                <Grid.Col span={4} >
                    <Image src="https://raw.githubusercontent.com/mantinedev/mantine/master/.demo/images/bg-7.png"/>
                    <Title order={2} fz={"h3"} c={"gray.6"} my={"md"}>Work Link</Title>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                    <Title order={2} fz={"h3"} c={"gray.6"} my={"md"}>Skills</Title>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                    <Text>abc something</Text>
                </Grid.Col>
                <Grid.Col offset={1} span={7} >
                    <Stack gap={"xl"}>
                    <TextInput label="Email" placeholder="Your email"
                        value={username}
                        onChange={(event) => setUsername(event.currentTarget.value)}
                    />
                
                    <PasswordInput
                        label="Password"
                        placeholder="Input placeholder"
                        value={password}
                        onChange={(event) => setPassword(event.currentTarget.value)}
                    />

                    <Button variant="filled" radius={"xl"} onClick={handleLogin}>Login</Button>
                    
                    </Stack>
                </Grid.Col>
            </Grid>
        </Container>
    )
}

export default Login
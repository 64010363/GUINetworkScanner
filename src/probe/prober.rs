use serde::{
    Deserialize,
    Serialize
};
use serde_json::to_string;
use std::net::Ipv4Addr;
use std::sync::mpsc::{
    channel, 
    Receiver, 
    Sender
};
use std::thread::{Builder, JoinHandle};
use std::{
    process, 
    time::Duration
};

mod icmp_ping;
mod rand_ping;
mod window_ping;

#[derive(Serialize, Deserialize)]
pub struct Prober {
    name: String,
    addr_set: Vec<Ipv4Addr>,
}

impl Prober {
    fn thread_builder(
        &self,
        addr: Ipv4Addr,
        thread_id: usize,
    ) -> JoinHandle<Option<Ipv4Addr>> {
        let builder: Builder = Builder::new()
            .name(thread_id.to_string())
            .stack_size(32 * 1024);

        match builder.spawn(move || {
            window_ping::ping(addr)
        }) {
            Ok(handler) => handler,
            Err(e) => {
                eprintln!("Thread Allocation failed due to {:?}", e);
                process::exit(12);
            }
        }
    }

    fn thread_listener(length: usize, rx: Receiver<Ipv4Addr>) -> Vec<Ipv4Addr> {
        let mut result: Vec<Ipv4Addr> = Vec::new();
        let time: Duration = Duration::new(0, 030_000_000);

        for _ in 0..length {
            if let Ok(val) = rx.recv_timeout(time) {
                result.push(val);
            }
        }
        result
    }

    fn thread_joiner(handler_list: Vec<JoinHandle<Option<Ipv4Addr>>>) -> Vec<Ipv4Addr>
    {
        let mut result_vec: Vec<Ipv4Addr> = Vec::with_capacity(256);

        for handler in handler_list {
            match handler.join() {
                Ok(val) => {
                    match val {
                        Some(ipaddr) => {
                            result_vec.push(ipaddr);
                        }
                        None => {}
                    }
                }
                Err(_) => {}
            }
            
        }
        result_vec
    }

    pub fn probe(&self) -> Result<String, serde_json::Error> {
        let length: usize = self.addr_set.len();
        let result_list: Vec<Ipv4Addr>;
        let prober_res: Prober;
        let mut handler_list: Vec<JoinHandle<Option<Ipv4Addr>>> = Vec::new();
        let mut handler: JoinHandle<Option<Ipv4Addr>>;

        for i in 0..length {
            handler = Prober::thread_builder(&self, self.addr_set[i].clone(), i);
            handler_list.push(handler)
        }
        result_list = Prober::thread_joiner(handler_list);
        prober_res = Prober {
            name: self.name.clone(),
            addr_set: result_list
        };
        to_string(&prober_res)
    }
}

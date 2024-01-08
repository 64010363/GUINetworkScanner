use std::thread::{
	Builder,
	JoinHandle
};
use std::net::IpAddr;
use std::any::Any;
use std::process;

pub type JoinHd = JoinHandle<Vec<u16>>;
pub type ScanFunc = fn(&IpAddr, Vec<u16>) -> Vec<u16>;
type JoinErr = Box<(dyn Any + Send + 'static)>;
type JoinRes = Result<Vec<u16>, JoinErr>;

pub fn thread_builder(ip: IpAddr, subset: Vec<u16>, subset_name: String, func: ScanFunc) -> JoinHd
{
	let builder: Builder = Builder::new()
							.name(subset_name)
							.stack_size(32 * 1024);

	match builder.spawn(move || { func(&ip, subset) })
	{
		Ok(thread_hander) => thread_hander,
		Err(e) => {
			eprintln!("Thread Allocation failed due to {:?}", e);
			process::exit(1);
		}
	}
}

pub fn thread_joiner(thread_hd_list: Vec<JoinHd>) -> Vec<u16>
{
	let mut result: JoinRes;
	let mut result_list: Vec<JoinRes> = Vec::new();
	let mut port_result: Vec<u16> = Vec::new();

	for handler in thread_hd_list
	{
		result = handler.join();
		result_list.push(result);
	}
	
	for res in result_list
	{
		match res
		{
			Ok(ports) => port_result.extend(ports),
			Err(_) => {}
		}
	}
	return port_result;
}
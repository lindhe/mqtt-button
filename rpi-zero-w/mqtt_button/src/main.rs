use clap::Parser;

/// Sends an MQTT message upon buttonpress
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Hostname to MQTT server
    #[arg(short = 'H', long)]
    hostname: String,

    /// GPIO pin for the button
    #[arg(short, long)]
    gpio_pin: u8,

    /// Invert button state (default: closed circuit == pressed)
    #[arg(long)]
    inverted: bool,

    /// Payload for MQTT message when button is pressed
    #[arg(short, long, default_value = "PRESSED")]
    pressed_message: String,

    /// Payload for MQTT message when button is released
    #[arg(short, long, default_value = "RELEASED")]
    released_message: String,

    /// Use keyboard input instead of GPIO button
    #[arg(long)]
    mocked: bool,

    /// MQTT topic to publish to
    #[arg(short, long)]
    topic: String,
}

fn main() {
    let args = Args::parse();

    for _ in 0..args.gpio_pin {
        println!("Hello {}!", args.hostname)
    }
}

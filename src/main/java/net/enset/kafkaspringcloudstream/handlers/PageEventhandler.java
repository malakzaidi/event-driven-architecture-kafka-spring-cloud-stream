package net.enset.kafkaspringcloudstream.handlers;


import net.enset.kafkaspringcloudstream.events.PageEvent;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;

import java.util.function.Consumer;

@Component
public class PageEventhandler {
    @Bean
    public Consumer<PageEvent> pageEventConsumer(){
        return (input) ->{
            System.out.println("*******************");
            System.out.println(input.toString());
            System.out.println("*******************");
        };
    }
}

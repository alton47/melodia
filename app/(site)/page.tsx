import Header from "@/components/Header";
import ListItem from "@/components/ListItem";
import React from "react";

const page = () => {
  return (
    <div className="bg-neutral-900 rounded-lg h-full w-full overflow-hidden overflow-y-auto">
      <Header>
        <div className="mb-2">
          <h1 className="text-white text-3xl font-semibold">Welcome bitch</h1>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3 mt-4">
            <ListItem
              image="/images/liked.jpeg"
              name="Liked songs"
              href="liked"
            />
          </div>
        </div>
      </Header>
      <div className="mt-2 mb-7 px-6">
        <div className="flex justify-between items-center">
          <h1 className="text-white text-2xl font-semibold">Ngoma mpyaa</h1>
        </div>
        <div>List ya Ngomaa</div>
      </div>
    </div>
  );
};

export default page;
